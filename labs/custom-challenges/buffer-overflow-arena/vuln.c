#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

// Disable buffering on stdout/stdin so netcat/socat output flushes immediately
void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

// Target function for ret2win exploit
void print_flag() {
    char flag[128];
    FILE *f = fopen("/flag.txt", "r");
    if (f == NULL) {
        printf("\n[!] Error: Flag file not found. Contact administrator.\n");
        exit(1);
    }
    fgets(flag, sizeof(flag), f);
    fclose(f);
    printf("\n=======================================================\n");
    printf("🎯 SUCCESS! Control flow redirected to print_flag()!\n");
    printf("🚩 FLAG: %s", flag);
    printf("=======================================================\n\n");
    exit(0);
}

void vulnerable_function() {
    char buffer[64];
    
    printf("\n[+] Allocated 64-byte stack buffer at: %p\n", (void*)buffer);
    printf("[+] Target print_flag() function is located at: %p\n", (void*)&print_flag);
    printf("[?] Enter your feedback or payload: ");
    
    // VULNERABILITY: gets() does not check buffer boundary
    gets(buffer);
    
    printf("\n[*] Received: %s\n", buffer);
    printf("[*] Returning from function... Goodbye!\n");
}

int main() {
    setup();
    printf("=======================================================\n");
    printf("   ⚡ PWN ARENA: 64-BIT STACK BUFFER OVERFLOW (RET2WIN)   \n");
    printf("=======================================================\n");
    printf("Target Architecture: x86_64 Linux\n");
    printf("Protection: No Stack Canary (-fno-stack-protector), No PIE (-no-pie)\n");
    
    vulnerable_function();
    return 0;
}

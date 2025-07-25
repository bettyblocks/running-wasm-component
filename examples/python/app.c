#include <stdio.h>

int main(int argc, char **argv) {
    if (argc > 1) {
        printf("Received JSON: %s\n", argv[1]);
    } else {
        printf("No input provided.\n");
    }
    return 0;
}

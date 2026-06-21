class BrainfuckInterpreter {
  // The memory tape (30,000 bytes initialized to 0)
  private tape: Uint8Array = new Uint8Array(30000);
  private dataPointer: number = 0;
  private instructionPointer: number = 0;
  private output: string = "";

  public run(code: string): string {
    this.output = "";
    this.dataPointer = 0;
    this.instructionPointer = 0;
    this.tape.fill(0);

    // Clean the input to keep only valid commands
    const instructions = code.replace(/[^+\-<>.,[\]]/g, '');

    while (this.instructionPointer < instructions.length) {
      const char = instructions[this.instructionPointer];

      switch (char) {
        case '>':
          this.dataPointer++;
          break;
        case '<':
          this.dataPointer--;
          break;
        case '+':
          this.tape[this.dataPointer]++;
          break;
        case '-':
          this.tape[this.dataPointer]--;
          break;
        case '.':
          // Convert the byte value to an ASCII character
          this.output += String.fromCharCode(this.tape[this.dataPointer]);
          break;
        case '[':
          // Jump forward to matching ']' if current byte is 0
          if (this.tape[this.dataPointer] === 0) {
            let loopCount = 1;
            while (loopCount > 0) {
              this.instructionPointer++;
              if (instructions[this.instructionPointer] === '[') loopCount++;
              if (instructions[this.instructionPointer] === ']') loopCount--;
            }
          }
          break;
        case ']':
          // Jump backward to matching '[' if current byte is NOT 0
          if (this.tape[this.dataPointer] !== 0) {
            let loopCount = 1;
            while (loopCount > 0) {
              this.instructionPointer--;
              if (instructions[this.instructionPointer] === ']') loopCount++;
              if (instructions[this.instructionPointer] === '[') loopCount--;
            }
          }
          break;
      }
      this.instructionPointer++;
    }

    return this.output;
  }
}

// --- Run the Interpreter ---
const bf = new BrainfuckInterpreter();

// This is Brainfuck code that prints "Hello World!"
const helloWorldCode = `
++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]
>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.
`;

console.log("--- Brainfuck Output ---");
console.log(bf.run(helloWorldCode));

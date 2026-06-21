class MiniParser {
  // A collection of rules: [Regex pattern, HTML replacement string]
  private rules: [RegExp, string][] = [
    [/# (.*)/g, '<h1>$1</h1>'],                 // # Header
    [/## (.*)/g, '<h2>$1</h2>'],                // ## Subheader
    [/\*\*(.*?)\*\*/g, '<strong>$1</strong>'],   // **Bold**
    [/\*(.*?)\*/g, '<em>$1</em>'],              // *Italics*
    [/`(.*?)`/g, '<code>$1</code>']             // `Inline Code`
  ];

  public parse(markdown: string): string {
    let html = markdown;

    // Apply each rule to the text
    for (const [regex, replacement] of this.rules) {
      html = html.replace(regex, replacement);
    }

    // Handle paragraphs for lines that didn't get wrapped in HTML tags yet
    return html
      .split('\n')
      .map(line => {
        if (line.trim() === '') return '';
        if (line.startsWith('<')) return line; // Already an HTML tag
        return `<p>${line}</p>`;
      })
      .join('\n');
  }
}

// --- Run the Parser ---
const parser = new MiniParser();

const rawMarkdown = `
# Project Notes
This is a **simple** parser written in *TypeScript*.
You can write \`code\` blocks too.
## Section 2
Everything gets converted smoothly.
`;

const outputHTML = parser.parse(rawMarkdown);
console.log("--- Generated HTML ---");
console.log(outputHTML);

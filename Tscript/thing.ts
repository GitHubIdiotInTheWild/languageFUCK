type Grid = { [cell: string]: string | number };

class MiniExcel {
  private sheet: Grid = {};

  // Formulas
  public set(cell: string, value: string | number): void {
    this.sheet[cell.toUpperCase()] = value;
  }

  // Get and resolve the value of a cell
  public get(cell: string): number {
    const rawValue = this.sheet[cell.toUpperCase()];

    if (rawValue === undefined) return 0;
    if (typeof rawValue === 'number') return rawValue;

    // If it's a formula like "=A1+B1"
    if (typeof rawValue === 'string' && rawValue.startsWith('=')) {
      return this.evaluateFormula(rawValue);
    }

    return parseFloat(rawValue) || 0;
  }

  // A simple formula parser for addition
  private evaluateFormula(formula: string): number {
    // Remove '=' and split by '+'
    const expression = formula.substring(1);
    const parts = expression.split('+');

    return parts.reduce((sum, part) => {
      const trimmed = part.trim();
      // If the part is a cell reference (like A1), fetch its value; otherwise parse as number
      const isCell = /[A-Z]+\d+/.test(trimmed);
      const val = isCell ? this.get(trimmed) : parseFloat(trimmed);
      return sum + (isNaN(val) ? 0 : val);
    }, 0);
  }

  // Print the current active sheet state
  public dump(): void {
    console.log("--- Spreadsheet State ---");
    for (const key of Object.keys(this.sheet).sort()) {
      console.log(`${key}: ${this.sheet[key]} => (Evaluates to: ${this.get(key)})`);
    }
  }
}

// --- Run the Spreadsheet ---
const excel = new MiniExcel();

excel.set("A1", 40);
excel.set("B1", 2);
excel.set("C1", "=A1+B1"); // Dynamic formula
excel.set("D1", "=C1+10");  // Chained formula

excel.dump();

console.log("\nUpdating A1 to 100...");
excel.set("A1", 100); // Everything updating automatically on evaluation
excel.dump();

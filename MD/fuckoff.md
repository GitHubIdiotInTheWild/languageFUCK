# Random Language Snippets

A quick markdown dump of code snippets from jscript, python, Lua, java, and tscript.

## JavaScript: util

```javascript
const randomInt = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;

const pickRandom = (array) => array[Math.floor(Math.random() * array.length)];

const words = ['alpha', 'bravo', 'charlie', 'delta'];
console.log('Random word:', pickRandom(words));
console.log('Random number:', randomInt(1, 10));
```

## Python: cd gen

```python
def countdown(n):
    while n > 0:
        yield n
        n -= 1

for value in countdown(5):
    print(value)
```

## Lua: simple table iteration

```lua
local items = {"red", "green", "blue"}
for index, value in ipairs(items) do
    print(index, value)
end
```

## TypeScript: typed record

```ts
type User = {
  id: number;
  name: string;
  active: boolean;
};

const users: User[] = [
  { id: 1, name: 'Mira', active: true },
  { id: 2, name: 'Kai', active: false },
];

const activeUsers = users.filter((user) => user.active);
console.log(activeUsers);
```

## Java: one-liner main

```java
public class RandomSnippet {
    public static void main(String[] args) {
        System.out.println("Hello from Java snippet!");
    }
}
```

## note

bored asf so before i get to the REAL shit i made this :D:D:D:D:D
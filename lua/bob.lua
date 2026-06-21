-- bob.lua: A simple text-based game to learn Lua
-- Demonstrates: tables, functions, loops, string manipulation, basic OOP

-- Game state
local game = {
  player_name = "",
  health = 100,
  gold = 0,
  inventory = {},
  location = "village"
}

-- Locations map
local locations = {
  village = {
    name = "Village Square",
    description = "A peaceful village. You see a merchant, a forest, and a tavern.",
    exits = { forest = "north", tavern = "east" }
  },
  forest = {
    name = "Dark Forest",
    description = "Dark trees surround you. You hear wolves howling.",
    exits = { village = "south" }
  },
  tavern = {
    name = "The Rusty Tavern",
    description = "Warm ale and laughter. A bartender eyes you curiously.",
    exits = { village = "west" }
  }
}

-- Helper functions
local function print_separator()
  print(string.rep("-", 40))
end

local function table_keys(t)
  local keys = {}
  for k, _ in pairs(t) do
    table.insert(keys, k)
  end
  return keys
end

local function get_location()
  return locations[game.location]
end

local function describe_location()
  local loc = get_location()
  print_separator()
  print("📍 " .. loc.name)
  print(loc.description)
  print_separator()
  print("Exits:", table.concat(table_keys(loc.exits), ", "))
end

local function add_item(item_name)
  table.insert(game.inventory, item_name)
  print("✓ Added: " .. item_name)
end

local function show_inventory()
  print_separator()
  print("📦 Inventory (" .. #game.inventory .. "/" .. 10 .. ")")
  if #game.inventory == 0 then
    print("  (empty)")
  else
    for i, item in ipairs(game.inventory) do
      print("  " .. i .. ". " .. item)
    end
  end
  print("💰 Gold: " .. game.gold)
  print("❤️  Health: " .. game.health)
  print_separator()
end

local function move(direction)
  local loc = get_location()
  local new_location = nil

  for place, dir in pairs(loc.exits) do
    if dir == direction or place == direction then
      new_location = place
      break
    end
  end

  if new_location then
    game.location = new_location
    print("→ Moved " .. direction .. "...")
    describe_location()
  else
    print("❌ Can't go " .. direction .. " from here.")
  end
end

local function explore()
  local loc = game.location
  local random_items = {
    { name = "Gold Coin", gold = 10 },
    { name = "Rusty Sword", gold = 0 },
    { name = "Healing Potion", gold = 0 },
    { name = "Ancient Map", gold = 0 }
  }

  local item = random_items[math.random(#random_items)]
  add_item(item.name)
  game.gold = game.gold + item.gold
  print("Found: " .. item.name)
end

local function show_help()
  print_separator()
  print("Commands:")
  print("  help         - show this menu")
  print("  look         - describe current location")
  print("  north|south|east|west - move")
  print("  inventory    - show items and gold")
  print("  explore      - search location for items")
  print("  status       - show game status")
  print("  quit         - exit game")
  print_separator()
end

local function show_status()
  print_separator()
  print("Player: " .. game.player_name)
  print("Location: " .. get_location().name)
  print("Health: " .. game.health)
  print("Gold: " .. game.gold)
  print("Items: " .. #game.inventory)
  print_separator()
end

-- Main game loop
local function run()
  print("🎮 Welcome to Lua Adventure Game!")
  print_separator()

  io.write("What is your name, adventurer? ")
  game.player_name = io.read()

  print("\n✨ Welcome, " .. game.player_name .. "!")
  describe_location()
  show_help()

  while true do
    io.write("\n> ")
    local input = io.read()
    local command = string.lower(input)

    if command == "quit" or command == "exit" then
      print("\n👋 Goodbye, " .. game.player_name .. "!")
      break
    elseif command == "help" then
      show_help()
    elseif command == "look" then
      describe_location()
    elseif command == "inventory" then
      show_inventory()
    elseif command == "explore" then
      explore()
    elseif command == "status" then
      show_status()
    elseif command == "north" or command == "south" or command == "east" or command == "west" then
      move(command)
    else
      print("❌ Unknown command. Type 'help' for options.")
    end
  end
end

-- Start the game
run()

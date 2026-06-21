math.randomseed(math.floor(os.time() + os.clock() * 1000))

local function wait(seconds)
    os.execute("sleep " .. tonumber(seconds))
end

local function random_wait_time()
    return math.random(1, 4)
end

print("SUBSCRIBE")
wait(0.2)
print("--------------------------------------------------")

local inventory = { "golden toilet", "caitlyn's hat", "the conductor's uniform", "half-eaten taco", "dusty floppy disk", "an existential crisis", "pet rock" }

local random_index = math.random(1, #inventory)
local random_item = inventory[random_index]

print("You searched the void and found: " .. random_item)

local message1 = "Yeah, you should definitely sell that."
local message2 = "Damn. Collector's item.. Probably should give that to sirshithol."
local message3 = "Hm. You should give that to sirshithol. Unless he's already wearing something else. He'll ask for it later."

local function gtm()
    print(message1)
end

local function chm()
    print(message2)
end

local function tcum()
    print(message3)
end

if random_index == 1 then
    wait(0.5)
    gtm()
elseif random_index == 2 then
    wait(0.5)
    chm()
elseif random_index == 3 then
    wait(0.5)
    tcum()
end

wait(1.5)

print("Self-destructing in T-3.")
wait(1)
print("Self-destructing in T-2..")
wait(1)
print("Self-destructing in T-1...")
wait(1)
print("Just kidding, the script is fine.")

wait(1.75)

local function simulate_glitch()
    local glitch_chance = math.random(1, 10)
    local error_count = math.random(1, 9)
    if glitch_chance > 5 then
        return error_count .. " error(s) found.", true
    else
        return "0 errors found.", false
    end
end

local system_pool = {1, 2, 3, 4, 5}

local function systemoffline()
    local pool_index = math.random(1, #system_pool)
    local chosen_system = system_pool[pool_index]
    
    table.remove(system_pool, pool_index)
    
    print("System " .. chosen_system .. " offline.")
end

local function systemonline()
    local pool_index = math.random(1, #system_pool)
    local chosen_system = system_pool[pool_index]
    
    table.remove(system_pool, pool_index)
    
    print("System " .. chosen_system .. " online.")
end

local function loading_dots()
    local messages = {
        "Loading...",
        "Starting...",
        "Working..."
    }
    
    local random_indexpm = math.random(1, #messages)
    local random_pm = messages[random_indexpm]
    print("...")
    wait(0.6)
    print(random_pm)
end

print("Diagnostic scan scheduled. Running.")
wait(1.3)
print("Terminating all systems...")
wait(1)
systemoffline()
wait(0.3)
systemoffline()
wait(0.3)
systemoffline()
wait(0.7)
systemoffline()
wait(0.4)
systemoffline()
wait(random_wait_time())
print("All systems offline. Running diagnostic scan..")
wait(0.2)
loading_dots()

wait(1)

local glitch_message, has_errors = simulate_glitch()
print("Scan Result: " .. glitch_message)
wait(1)

if has_errors then
    print("Initiating hotfixes... Please hold.")
    wait(random_wait_time())
    print("Patch successful.")
    wait(1.8)
end

system_pool = {1, 2, 3, 4, 5}

print("Rebooting core systems...")
wait(random_wait_time())
systemonline()
wait(random_wait_time())
systemonline()
wait(random_wait_time())
systemonline()
wait(random_wait_time())
systemonline()
wait(random_wait_time())
systemonline()
wait(1.4)
print("System check 1.")
wait(1)
print("Success.")
wait(0.2)
print("System check 2.")
wait(4.5)
print("Success.")
wait(0.2)
print("System check 3 [FINAL]")
wait(7)
print("Success.")
wait(0.4)
print("All systems back online.")
wait(random_wait_time())
print("GET OUT")

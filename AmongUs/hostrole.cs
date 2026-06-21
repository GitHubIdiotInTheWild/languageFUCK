using System;
using System.Collections.Generic;
using BepInEx;
using BepInEx.IL2CPP;
using HarmonyLib;

namespace AmongUsHostMenuMod
{
    // Registers your mod with BepInEx so the game loads it
    [BepInPlugin("com.yourname.amongus.hostoverride", "Host Role Override", "1.0.0")]
    public class HostOverridePlugin : BasePlugin
    {
        public Harmony Harmony { get; } = new Harmony("com.yourname.amongus.hostoverride");

        // Simple dictionary to store which Player ID gets which Role ID
        // Role ID Examples: 0 = Crewmate, 1 = Impostor, 2 = Scientist, 3 = Engineer, 4 = Guardian Angel
        public static Dictionary<byte, int> SelectedRoles = new Dictionary<byte, int>();

        public override void Load()
        {
            // Tells Harmony to scan this code for any game hacks/patches
            Harmony.PatchAll();
            Log.LogInfo("Host Role Override Mod Loaded Successfully!");
        }
    }

    // This intercepts the role assignment phase right as the game starts
    [HarmonyPatch(typeof(RoleManager), nameof(RoleManager.SelectRoles))]
    public static class RoleManagerPatch
    {
        public static bool Prefix(RoleManager __instance)
        {
            // Only execute if WE are the host of the lobby
            if (!AmongUsClient.Instance.AmHost) return true; 

            // Loop through every player currently in the game
            foreach (var player in PlayerControl.AllPlayerControls)
            {
                byte id = player.PlayerId;

                // Check if the host selected a custom role for this specific player ID
                if (HostOverridePlugin.SelectedRoles.TryGetValue(id, out int forcedRole))
                {
                    // Force the game to assign that specific role to the player
                    player.RpcSetRole((RoleTypes)forcedRole);
                }
            }

            // Return true lets the game handle assigning roles to anyone else left over
            return true;
        }
    }
}
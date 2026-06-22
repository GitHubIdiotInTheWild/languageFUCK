using System;
using BepInEx;
using BepInEx.Unity.IL2CPP;
using HarmonyLib;

namespace hostrole
{
    [BepInPlugin("com.coinpunch.hostrole", "HostRole", "1.0.0")]
    public class HostRolePlugin : BasePlugin
    {
        // 0 = Random, 1 = Crewmate, 2 = Impostor
        public static int SelectedRoleType = 0; 
        public static string SelectedSpecificRole = "Random";

        public override void Load()
        {
            var harmony = new Harmony("com.coinpunch.hostrole");
            harmony.PatchAll();
        }
    }

    [HarmonyPatch("RoleManager", "SelectRoles")]
    public static class RoleManagerPatch
    {
        [HarmonyPrefix]
        public static bool Prefix(object __instance)
        {
            // If random is selected, let the game handle it normally
            if (HostRolePlugin.SelectedRoleType == 0) return true;

            try
            {
                // Find the local client dynamically
                var clientType = AccessTools.TypeByName("AmongUsClient");
                var instanceProp = AccessTools.Property(clientType, "Instance");
                var clientInstance = instanceProp.GetValue(null);
                var localPlayerProp = AccessTools.Property(clientType, "LocalPlayer");
                var localPlayer = localPlayerProp.GetValue(clientInstance);

                if (localPlayer == null) return true;

                // Find the object property on the player
                var playerObjProp = AccessTools.Property(localPlayer.GetType(), "Object");
                var playerObj = playerObjProp.GetValue(localPlayer);

                // Find the RoleManager component on the player object
                var roleManagerProp = AccessTools.Property(playerObj.GetType(), "RoleManager");
                var roleManager = roleManagerProp.GetValue(playerObj);
                var setRoleMethod = AccessTools.Method(roleManager.GetType(), "SetRole");

                // Get the exact Role enum type dynamically
                var roleEnumType = AccessTools.TypeByName("RoleTypes");

                if (HostRolePlugin.SelectedRoleType == 1 && HostRolePlugin.SelectedSpecificRole == "Random")
                {
                    var crewmateRole = Enum.Parse(roleEnumType, "Crewmate");
                    setRoleMethod.Invoke(roleManager, new object[] { crewmateRole });
                }
                else if (HostRolePlugin.SelectedRoleType == 2 && HostRolePlugin.SelectedSpecificRole == "Random")
                {
                    var impostorRole = Enum.Parse(roleEnumType, "Impostor");
                    setRoleMethod.Invoke(roleManager, new object[] { impostorRole });
                }
                else if (HostRolePlugin.SelectedSpecificRole != "Random")
                {
                    var customRole = Enum.Parse(roleEnumType, HostRolePlugin.SelectedSpecificRole);
                    setRoleMethod.Invoke(roleManager, new object[] { customRole });
                }

                return false; // Skip original random logic for the host
            }
            catch (Exception)
            {
                // Fallback to normal behavior if reflection fails
                return true;
            }
        }
    }
}
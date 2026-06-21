using System;
using System.Collections.Generic;
using BepInEx;
using BepInEx.IL2CPP;
using HarmonyLib;

namespace AmongUsHostMenuMod
{
    [BepInPlugin("com.yourname.amongus.hostoverride", "Host Role Override", "1.0.0")]
    public class HostOverridePlugin : BasePlugin
    {
        public static Dictionary<byte, int> SelectedRoles = new Dictionary<byte, int>();

        public override void Load()
        {
            var harmony = new Harmony("com.yourname.amongus.hostoverride");
            harmony.PatchAll();
        }
    }

    [HarmonyPatch(typeof(RoleManager), nameof(RoleManager.SelectRoles))]
    public static class RoleManagerPatch
    {
        public static bool Prefix(RoleManager __instance)
        {
            if (!AmongUsClient.Instance.AmHost) return true; 

            foreach (var player in PlayerControl.AllPlayerControls)
            {
                byte id = player.PlayerId;

                if (HostOverridePlugin.SelectedRoles.TryGetValue(id, out int forcedRole))
                {
                    player.RpcSetRole((RoleTypes)forcedRole);
                }
            }
            return true;
        }
    }
}
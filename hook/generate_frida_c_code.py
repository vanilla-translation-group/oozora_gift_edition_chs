import sys

if len(sys.argv) != 4:
    print("usage: ./generate_frida_c_code.py <JS File> <Target EXE> <Script Name>")
    exit(1)

converted_script = ""

with open(sys.argv[1]) as f:
    for i in f.readlines():
        converted_script += "        \"" + "".join([j.encode("unicode-escape").decode().replace("\"", "\\\"").replace("\\u", "\\\\u") for j in i]) + "\"\n"

with open(f"{sys.argv[3]}.c", "w") as f:
    f.write(f"""#include "frida-core.h"

#include <stdlib.h>
#include <string.h>

#ifndef _DEBUG
#pragma comment(linker, "/subsystem:\\"windows\\" /entry:\\"mainCRTStartup\\"")
#endif

static void on_detached(FridaSession *session, FridaSessionDetachReason reason, FridaCrash *crash, gpointer user_data);
static void on_message(FridaScript *script, const gchar *message, GBytes *data, gpointer user_data);
static void on_signal(int signo);
static gboolean stop(gpointer user_data);

static GMainLoop *loop = NULL;

int main(int argc, char *argv[]) {{
  guint target_pid;
  FridaDeviceManager *manager;
  GError *error = NULL;
  FridaDeviceList *devices;
  gint num_devices, i;
  FridaDevice *local_device;
  FridaSession *session;

  frida_init();

  loop = g_main_loop_new(NULL, TRUE);

  signal(SIGINT, on_signal);
  signal(SIGTERM, on_signal);

  manager = frida_device_manager_new();

  devices = frida_device_manager_enumerate_devices_sync(manager, NULL, &error);
  g_assert(error == NULL);

  local_device = NULL;
  num_devices = frida_device_list_size(devices);
  for (i = 0; i != num_devices; i++) {{
    FridaDevice *device = frida_device_list_get(devices, i);

    g_print("[*] Found device: \\"%s\\"\\n", frida_device_get_name(device));

    if (frida_device_get_dtype(device) == FRIDA_DEVICE_TYPE_LOCAL)
      local_device = g_object_ref(device);

    g_object_unref(device);
  }}
  g_assert(local_device != NULL);

  frida_unref(devices);
  devices = NULL;

  target_pid = frida_device_spawn_sync(local_device, "{sys.argv[2]}", NULL, NULL, &error);
  g_assert(error == NULL);

  session = frida_device_attach_sync(local_device, target_pid, NULL, NULL, &error);
  if (error == NULL) {{
    FridaScript *script;
    FridaScriptOptions *options;

    g_signal_connect(session, "detached", G_CALLBACK(on_detached), NULL);
    if (frida_session_is_detached(session))
      goto session_detached_prematurely;

    g_print("[*] Attached\\n");

    options = frida_script_options_new();
    frida_script_options_set_name(options, "{sys.argv[3]}");
    frida_script_options_set_runtime(options, FRIDA_SCRIPT_RUNTIME_QJS);

    script = frida_session_create_script_sync(session,
        {converted_script.strip()},
        options, NULL, &error);
    g_assert(error == NULL);

    g_clear_object(&options);

    g_signal_connect(script, "message", G_CALLBACK(on_message), NULL);

    frida_script_load_sync(script, NULL, &error);
    g_assert(error == NULL);

    g_print("[*] Script loaded\\n");

    frida_device_resume_sync(local_device, target_pid, NULL, &error);
    g_assert(error == NULL);

    if (g_main_loop_is_running(loop))
      g_main_loop_run(loop);

    g_print("[*] Stopped\\n");

    frida_script_unload_sync(script, NULL, NULL);
    frida_unref(script);
    g_print("[*] Unloaded\\n");

    frida_session_detach_sync(session, NULL, NULL);
session_detached_prematurely:
    frida_unref(session);
    g_print("[*] Detached\\n");
  }}
  else {{
    g_printerr("Failed to attach: %s\\n", error->message);
    g_error_free(error);
  }}

  frida_unref(local_device);

  frida_device_manager_close_sync(manager, NULL, NULL);
  frida_unref(manager);
  g_print("[*] Closed\\n");

  g_main_loop_unref(loop);

  return 0;
}}

static void on_detached(FridaSession *session,
                        FridaSessionDetachReason reason,
                        FridaCrash *crash,
                        gpointer user_data) {{
  gchar *reason_str;

  reason_str = g_enum_to_string(FRIDA_TYPE_SESSION_DETACH_REASON, reason);
  g_print("on_detached: reason=%s crash=%p\\n", reason_str, crash);
  g_free(reason_str);

  g_idle_add(stop, NULL);
}}

static void on_message(FridaScript *script, const gchar *message, GBytes *data, gpointer user_data) {{
  JsonParser *parser;
  JsonObject *root;
  const gchar *type;

  parser = json_parser_new();
  json_parser_load_from_data(parser, message, -1, NULL);
  root = json_node_get_object(json_parser_get_root(parser));

  type = json_object_get_string_member(root, "type");
  if (strcmp(type, "log") == 0) {{
    const gchar *log_message;

    log_message = json_object_get_string_member(root, "payload");
    g_print("%s\\n", log_message);
  }}
  else {{
    g_print("on_message: %s\\n", message);
  }}

  g_object_unref(parser);
}}

static void on_signal(int signo) {{
  g_idle_add(stop, NULL);
}}

static gboolean stop(gpointer user_data) {{
  g_main_loop_quit(loop);

  return FALSE;
}}""")

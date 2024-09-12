#include <systemd/sd-bus.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>  // For usleep()

#define TARGET_BUS_NAME "org.freedesktop.systemd1"
#define OBJECT_PATH "/org/freedesktop/systemd1"
#define INTERFACE_NAME "org.freedesktop.systemd1.Manager"
#define METHOD_NAME "ListUnits"
#define ITERATION_LIMIT 100

static int __attribute__((noinline)) send_message(sd_bus *bus, sd_bus_message **msg)
{
    int ret;

    ret = sd_bus_message_new_method_call(bus, msg,
                                         TARGET_BUS_NAME,
                                         OBJECT_PATH,
                                         INTERFACE_NAME,
                                         METHOD_NAME);
    if (ret < 0) {
        fprintf(stderr, "Failed to create message: %s\n", strerror(-ret));
        return ret;
    }

    return 0;
}

static int __attribute__((noinline)) receive_message(sd_bus *bus, sd_bus_message *msg)
{
    sd_bus_error error = SD_BUS_ERROR_NULL;
    int ret;

    ret = sd_bus_call(bus, msg, 0, &error, &msg);
    if (ret < 0) {
        fprintf(stderr, "Failed to send message: %s\n", strerror(-ret));
        sd_bus_error_free(&error);
        return ret;
    }

    const char *expected_signature = "a(ssssssouso)";
    const char *received_signature = sd_bus_message_get_signature(msg, 1);

    if (strcmp(received_signature, expected_signature) != 0) {
        fprintf(stderr, "Unexpected message signature: %s\n", received_signature);
        return -1;
    }

    ret = sd_bus_message_enter_container(msg, SD_BUS_TYPE_ARRAY, "(ssssssouso)");
    if (ret < 0) {
        fprintf(stderr, "Failed to enter array container: %s\n", strerror(-ret));
        return ret;
    }

    const char *unit_name, *description, *load_state, *active_state, *sub_state;
    const char *following, *unit_path, *job_type, *job_path;
    unsigned int job_id;

    while ((ret = sd_bus_message_read(msg, "(ssssssouso)",
                                      &unit_name,
                                      &description,
                                      &load_state,
                                      &active_state,
                                      &sub_state,
                                      &following,
                                      &unit_path,
                                      &job_id,
                                      &job_type,
                                      &job_path)) > 0) {
        // printf("Unit: %s, Description: %s, Active: %s, SubState: %s, JobID: %u\n",
        //       unit_name, description, active_state, sub_state, job_id);
    }

    if (ret < 0) {
        fprintf(stderr, "Failed to read from message: %s\n", strerror(-ret));
        return ret;
    }

    ret = sd_bus_message_exit_container(msg);
    if (ret < 0) {
        fprintf(stderr, "Failed to exit array container: %s\n", strerror(-ret));
        return ret;
    }

    sd_bus_error_free(&error);
    return 0;
}

static int __attribute__((noinline)) process_dbus_message(sd_bus *bus)
{
    sd_bus_message *msg = NULL;
    int ret;

    ret = send_message(bus, &msg);
    if (ret < 0)
        return ret;

    ret = receive_message(bus, msg);
    if (ret < 0) {
        sd_bus_message_unref(msg);
        return ret;
    }

    sd_bus_message_unref(msg);
    return 0;
}

int main(int argc, char *argv[])
{
    sd_bus *bus = NULL;
    int ret;

    ret = sd_bus_open_system(&bus);
    if (ret < 0) {
        fprintf(stderr, "Failed to connect to system bus: %s\n", strerror(-ret));
        goto finish;
    }

    for (int i = 0; i < ITERATION_LIMIT; i++) {
        ret = process_dbus_message(bus);
        if (ret < 0)
            goto finish;

        usleep(1000 * 500);
    }

finish:
    sd_bus_unref(bus);
    return ret < 0 ? EXIT_FAILURE : EXIT_SUCCESS;
}


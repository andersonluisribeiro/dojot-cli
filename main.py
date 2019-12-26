import sys
from lib import Installer, Kafka, Gui, Cron, Kong, DeviceManager, Auth, Postgres, MongoDB, IoTAgentMQTT, IoTAgentLWM2M


installer = Installer(sys.argv)

if installer.is_for_configuration():

    try:

        installer.say_wellcome()
        installer.clone_repository()

        kafka = Kafka() \
            .show_name() \
            .ask_persistence_time() \
            .and_if_use_persistent_volume() \
            .and_volume_size()

        kong = Kong() \
            .show_name() \
            .ask_req_per_minute() \
            .ask_req_per_hour() \
            .ask_pg_username() \
            .ask_pg_password()

        devm = DeviceManager() \
            .show_name() \
            .ask_pg_username() \
            .ask_pg_password()

        auth = Auth() \
            .show_name() \
            .and_pg_username() \
            .and_pg_password() \
            .ask_if_should_send_mail() \
            .and_smtp_host() \
            .and_smtp_username() \
            .and_smtp_password() \
            .and_password_reset_link()

        postgres = Postgres() \
            .show_name() \
            .ask_super_username() \
            .and_super_password() \
            .and_if_use_persistent_volume() \
            .and_volume_size()

        mongo = MongoDB() \
            .show_name() \
            .ask_super_username() \
            .and_super_password() \
            .and_if_messages_will_be_persisted() \
            .and_persistence_time() \
            .and_if_use_persistent_volume() \
            .and_volume_size()

        gui = Gui() \
            .show_name() \
            .ask_use()

        mqtt = IoTAgentMQTT() \
            .show_name() \
            .ask_use() \
            .and_replicas() \
            .and_use_insecure_mqtt()   

        lwm2m = IoTAgentLWM2M() \
            .show_name() \
            .ask_use()

        cron = Cron() \
            .show_name() \
            .ask_use()

        installer \
            .create_vars_file_from(
                [kafka, kong, devm, auth, postgres, mongo, gui, mqtt, lwm2m, cron]
            ) \
            .call_ansible()

        installer.say_thanks()

    except KeyboardInterrupt:
        installer.say_bye()

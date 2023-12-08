# elementary

elementary is A meltano utility extension for elementary that wraps the `edr` command.

## Installing this extension for local development

1. Install the project dependencies with `poetry install`:

```shell
cd path/to/your/project
poetry install
```

2. Verify that you can invoke the extension:

```shell
poetry run elementary_extension --help
poetry run elementary_extension describe --format=yaml
poetry run elementary_invoker --help # if you have are wrapping another tool
poetry run elementary_extensions initialize
```

## Template updates

This project was generated with [copier](https://copier.readthedocs.io/en/stable/) from the [Meltano EDK template](https://github.com/meltano/edk).
Answers to the questions asked during the generation process are stored in the `.copier_answers.yml` file.

Removing this file can potentially cause unwanted changes to the project if the supplied answers differ from the original when using `copier update`.

## Configuration

```
 plugins:
    utilities:
      - name: elementary
        variant: elementary
        pip_url: elementary-data[bigquery] git+https://github.com/potloc/elementary-ext
        executable: elementary_invoker
        settings:
          - name: project_dir
            kind: string
            value: transform
          - name: profiles_dir
            kind: string
            value: transform/profiles
          - name: file_path
            kind: string
            value: output/elementary_report.html
          - name: skip_pre_invoke
            env: ELEMENTARY_EXT_SKIP_PRE_INVOKE
            kind: boolean
            value: true
            description:
              Whether to skip pre-invoke hooks which automatically run dbt clean
              and deps
          - name: slack-token
            kind: password
          - name: slack-channel-name
            kind: string
            value: elementary-notifs
          - name: google-service-account-path
            kind: string
          - name: gcs-bucket-name
            kind: string
          - name: days-back
            kind: string
          - name: env
            kind: string
        commands:
          initialize:
            args: initialize
            executable: elementary_extension
          describe:
            args: describe
            executable: elementary_extension
          monitor-report:
            args: monitor-report
            executable: elementary_extension
          monitor-send-report:
            args: monitor-send-report
            executable: elementary_extension
          send-report-gcs:
            send-report --google-service-account-path ${ELEMENTARY_GOOGLE_SERVICE_ACCOUNT_PATH}
            --gcs-bucket-name ${ELEMENTARY_GCS_BUCKET_NAME} --update-bucket-website true
            --executions-limit 5
          send-report-slack:
            send-report --slack-token ${ELEMENTARY_SLACK_TOKEN} --slack-channel-name ${ELEMENTARY_SLACK_CHANNEL_NAME}

        config:
          profiles-dir: transform/profiles/bigquery
          file-path: output/my-elementary-report.html
          slack-channel-name: my-channel-name
          google-service-account-path: .secrets/elementary-gcs.json
          gcs-bucket-name: my-storage-device
          skip_pre_invoke: true
          env: prod
          days-back: 3
```

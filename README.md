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
        namespace: elementary
        pip_url: elementary-data[bigquery]==0.5.3 git+https://github.com/potloc/elementary-ext.git
        executable: elementary_extension
        settings:
        - name: project_dir
          kind: string
          value: ${MELTANO_PROJECT_ROOT}/transform/profiles/bigquery/
        - name: profiles_dir
          kind: string
          value: ${MELTANO_PROJECT_ROOT}/transform/profiles/bigquery/
        - name: file_path
          kind: string
          value: ${MELTANO_PROJECT_ROOT}/utilities/elementary/report.html
        - name: skip_pre_invoke
          env: ELEMENTARY_EXT_SKIP_PRE_INVOKE
          kind: boolean
          value: true
          description: Whether to skip pre-invoke hooks which automatically run dbt clean and deps
        - name: slack-token
          kind: password
        - name: slack-channel-name
          kind: string
          value: elementary-notifs
        config:
          profiles-dir: ${MELTANO_PROJECT_ROOT}/transform/profiles/bigquery/
          file-path: ${MELTANO_PROJECT_ROOT}/utilities/elementary/report.html
          slack-channel-name: team-data-engineering-notifications
          skip_pre_invoke: true
        commands:
          monitor:
            description: Allows your to run monitoring with elementary
            args: monitor --profiles-dir ${ELEMENTARY_PROFILES_DIR}
          monitor-report:
            description: Allows your to create a local report
            args: monitor report
                  --profiles-dir ${ELEMENTARY_PROFILES_DIR}
                  --file-path ${ELEMENTARY_FILE_PATH}
          monitor-send-report:
            description: Allows your to send a report through slack
            args: monitor send-report
                  --profiles-dir ${ELEMENTARY_PROFILES_DIR}
                  --slack-token ${ELEMENTARY_SLACK_TOKEN}
                  --slack-channel-name ${ELEMENTARY_SLACK_CHANNEL_NAME}
```

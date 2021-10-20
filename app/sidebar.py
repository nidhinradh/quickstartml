import streamlit as st
import yaml


def render(config_path=""):
    configs = {}
    with st.sidebar:
        with open(config_path, "r") as stream:
            try:
                yaml_content = yaml.safe_load(stream)
                for sidebar_item in yaml_content["sidebar"]:
                    enable = False

                    if "enable_when" not in sidebar_item or (
                        "enable_when" in sidebar_item
                        and sidebar_item["enable_when"] == "always"
                    ):
                        enable = True
                    elif (
                        "enable_when" in sidebar_item
                        and sidebar_item["enable_when"] == "never"
                    ):
                        enable = False
                    else:
                        if sidebar_item["enable_when"]["condition"] == "is":
                            if (
                                configs[
                                    sidebar_item["enable_when"][
                                        "variable_name"
                                    ]
                                ]
                                == sidebar_item["enable_when"]["value"]
                            ):
                                enable = True
                        elif (
                            sidebar_item["enable_when"]["condition"]
                            == "is_not"
                        ):
                            if (
                                configs[
                                    sidebar_item["enable_when"][
                                        "variable_name"
                                    ]
                                ]
                                != sidebar_item["enable_when"]["value"]
                            ):
                                enable = True
                        elif sidebar_item["enable_when"]["condition"] == "in":
                            if (
                                configs[
                                    sidebar_item["enable_when"][
                                        "variable_name"
                                    ]
                                ]
                                in sidebar_item["enable_when"]["values"]
                            ):
                                enable = True
                        elif (
                            sidebar_item["enable_when"]["condition"]
                            == "not_in"
                        ):
                            if (
                                configs[
                                    sidebar_item["enable_when"][
                                        "variable_name"
                                    ]
                                ]
                                not in sidebar_item["enable_when"]["values"]
                            ):
                                enable = True

                    if enable:
                        if (sidebar_item["type"]) == "sub_heading":
                            st.subheader(sidebar_item["value"])

                        if (sidebar_item["type"]) == "checkbox":
                            configs[
                                sidebar_item["variable_name"]
                            ] = st.checkbox(
                                sidebar_item["label"],
                                value=sidebar_item["default"],
                            )

                        if (sidebar_item["type"]) == "radio":
                            configs[sidebar_item["variable_name"]] = st.radio(
                                sidebar_item["label"], sidebar_item["values"]
                            )

                        if (sidebar_item["type"]) == "slider":
                            configs[sidebar_item["variable_name"]] = st.slider(
                                sidebar_item["label"],
                                sidebar_item["min"],
                                sidebar_item["max"],
                                sidebar_item["default"],
                            )

                        if (sidebar_item["type"]) == "selectbox":
                            configs[
                                sidebar_item["variable_name"]
                            ] = st.selectbox(
                                sidebar_item["label"], sidebar_item["values"]
                            )

                        if (sidebar_item["type"]) == "number_input":
                            configs[
                                sidebar_item["variable_name"]
                            ] = st.number_input(
                                sidebar_item["label"],
                                value=sidebar_item["default"],
                                step=sidebar_item["step"],
                            )

                        if (sidebar_item["type"]) == "info":
                            st.info(sidebar_item["value"])

                        if (sidebar_item["type"]) == "warn":
                            st.warning(sidebar_item["value"])

                        if (sidebar_item["type"]) == "error":
                            st.error(sidebar_item["value"])

                        if (sidebar_item["type"]) == "success":
                            st.success(sidebar_item["value"])

            except yaml.YAMLError as error:
                st.error(error)

    return configs


if __name__ == "__main__":
    render(config_path="")

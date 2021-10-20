import importlib.util
import math
import base64
import streamlit as st
import re
import uuid


class Utils:
    @staticmethod
    def import_from_file(module_name, filepath):
        spec = importlib.util.spec_from_file_location(module_name, filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    @staticmethod
    def code_header(text):
        seperator_len = (75 - len(text)) / 2
        seperator_len_left = math.floor(seperator_len)
        seperator_len_right = math.ceil(seperator_len)
        return (
            f"# {'-' * seperator_len_left} {text} {'-' * seperator_len_right}"
        )

    @staticmethod
    def download_button(object_to_download, download_filename, button_text):
        try:
            b64 = base64.b64encode(object_to_download.encode()).decode()
        except AttributeError:
            b64 = base64.b64encode(object_to_download).decode()
        button_uuid = str(uuid.uuid4()).replace("-", "")
        button_id = re.sub("\d+", "", button_uuid)
        custom_css = f"""
            <style>
                #{button_id} {{
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    background-color: rgb(255, 255, 255);
                    color: rgb(38, 39, 48);
                    padding: .25rem .75rem;
                    position: relative;
                    text-decoration: none;
                    border-radius: 4px;
                    border-width: 1px;
                    border-style: solid;
                    border-color: rgb(230, 234, 241);
                    border-image: initial;
                }}
                #{button_id}:hover {{
                    border-color: rgb(246, 51, 102);
                    color: rgb(246, 51, 102);
                }}
                #{button_id}:active {{
                    box-shadow: none;
                    background-color: rgb(246, 51, 102);
                    color: white;
                    }}
            </style> """
        dl_link = (
            custom_css
            + f'<a download="{download_filename}" id="{button_id}" href="data:file/txt;base64,{b64}">{button_text}</a><br><br>'
        )
        st.markdown(dl_link, unsafe_allow_html=True)

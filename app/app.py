from importlib import util
import streamlit as st
import os
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from streamlit import config
from utils import Utils


load_dotenv()
utils = Utils()


class App:
    def __init__(self):
        self.app_banner = os.environ.get("APP_BANNER")
        self.app_title = os.environ.get("APP_TITLE")
        self.app_description = os.environ.get("APP_DESCRIPTION")
        self.templates_base_dir = os.environ.get("TEMPLATES_BASE_FOLDER")
        self.enabled_templates = os.environ.get("ENABLED_TEMPLATES").split("|")
        self.enabled_frameworks = os.environ.get("ENABLED_FRAMEWORKS")
        self.templates_file_name = os.environ.get("TEMPLATE_FILE_NAME")
        self.sidebar_file_name = os.environ.get("SIDEBAR_FILE_NAME")
        self.default_framework = os.environ.get("DEFAULT_FRAMEWORK")
        self.feedback_md_file = os.environ.get("FEEDBACK_MD_FILE")
        self.credits_md_file = os.environ.get("CREDITS_MD_FILE")
        self.sidebar_title = os.environ.get("SIDEBAR_TITLE")
        self.sidebar_template_menu_subheading = os.environ.get(
            "SIDEBAR_TEMPLATE_MENU_SUBHEADING"
        )
        self.sidebar_template_menu_selectbox_label = os.environ.get(
            "SIDEBAR_TEMPLATE_MENU_SELECTBOX_LABEL"
        )
        self.sidebar_framework_menu_selectbox_lebel = os.environ.get(
            "SIDEBAR_FRAMEWORK_MENU_SELECTBOX_LABEL"
        )
        self.configs = {}
        self.code_dir_path = ""
        self.selected_model_type = ""
        self.selected_framework = ""

    def load_main_content(self):
        st.set_page_config(
            page_title=self.app_title,
            page_icon=self.app_banner,
            layout="wide",
            initial_sidebar_state="expanded",
        )
        st.title(self.app_title)
        title_col, banner_col = st.columns([4, 2])
        title_col.write(self.app_description)
        with open(self.feedback_md_file, "r") as file:
            feedback_text = file.read()
            title_col.info(feedback_text)
        banner_col.image(self.app_banner)

    def load_sidebar(self):
        with st.sidebar:
            st.title(self.sidebar_title)
            st.subheader(self.sidebar_template_menu_subheading)
            self.selected_model_type = st.selectbox(
                self.sidebar_template_menu_selectbox_label,
                set(self.enabled_templates),
            )
            selected_template_path = os.path.join(
                self.templates_base_dir, self.selected_model_type
            )
            frameworks = [
                object.name
                for object in os.scandir(selected_template_path)
                if (object.is_dir() and object.name in self.enabled_frameworks)
            ]
            frameworks = sorted(
                frameworks, key=lambda framework: framework.lower()
            )
            self.selected_framework = st.selectbox(
                self.sidebar_framework_menu_selectbox_lebel,
                frameworks,
                index=0
                if self.default_framework not in frameworks
                else frameworks.index(self.default_framework),
            )
            self.code_dir_path = os.path.join(
                selected_template_path, self.selected_framework
            )
            config_sidebar = utils.import_from_file(
                module_name="config_sidebar", filepath="./app/sidebar.py"
            )
            self.configs = config_sidebar.render(
                config_path=os.path.join(
                    self.code_dir_path, self.sidebar_file_name
                )
            )

    def load_code(self):
        env = Environment(
            loader=FileSystemLoader(self.code_dir_path),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        template = env.get_template(self.templates_file_name)
        code = template.render(
            header=utils.code_header, notebook=False, **self.configs
        )
        if len(code) > 0:
            utils.download_button(
                code,
                self.selected_model_type
                + "_"
                + self.selected_framework
                + ".py",
                "Download Code",
            )
            st.code(code)

    def load_credits(self):
        with open(self.credits_md_file, "r") as file:
            credits_text = file.read()
            st.info(credits_text)

    def main(self):
        self.load_main_content()
        self.load_sidebar()
        self.load_code()
        self.load_credits()


app = App()
app.main()

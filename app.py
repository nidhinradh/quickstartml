import streamlit as st
import os
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
import utils
from markdown import markdown

load_dotenv()

app_banner = os.environ.get("APP_BANNER")
app_title = os.environ.get("APP_TITLE")
app_description = os.environ.get("APP_DESCRIPTION")
templates_base_dir = os.environ.get("TEMPLATES_BASE_FOLDER")
enabled_templates = os.environ.get("ENABLED_TEMPLATES").split("|")
enabled_frameworks = os.environ.get("ENABLED_FRAMEWORKS")
default_framework = os.environ.get("DEFAULT_FRAMEWORK")

st.set_page_config(page_title=app_title, page_icon = app_banner, layout = 'wide', initial_sidebar_state = 'expanded')
st.markdown(markdown.hide_streamlit_style, unsafe_allow_html=True)

col1, col2 = st.columns([5, 3])
col2.title(app_title)
col2.write(app_description)
col2.info('''
Feedback and questions help make you better at what you do!
###### 📬 Reach me at
[![Website Badge](http://img.shields.io/badge/-Website-blue?style=flat-square&logo=Google-Chrome&logoColor=white&link=https://nidhinradh.me/)](https://nidhinradh.me/) 
[![Instagram](http://img.shields.io/badge/-Instagram-purple?style=flat-square&logo=Instagram&logoColor=white&link=https://instagram.com/nidhinradh/)](https://instagram.com/nidhinradh/)
[![Facebook](http://img.shields.io/badge/-Facebook-blue?style=flat-square&logo=Facebook&logoColor=white&link=https://facebook.com/nidhinradh/)](https://facebook.com/nidhinradh/)
[![Github Badge](http://img.shields.io/badge/-Github-black?style=flat-square&logo=github&link=https://github.com/nidhinradh/)](https://github.com/nidhinradh/) 
[![Email Badge](https://img.shields.io/badge/-Email-d14836?style=flat-square&logo=Gmail&logoColor=white&link=mailto:hello@nidhinradh.me)](mailto:hello@nidhinradh.me)
[![Linkedin Badge](https://img.shields.io/badge/-LinkedIn-2781F4?style=flat-square&logo=LinkedIn&logoColor=white&link=https://www.linkedin.com/in/nidhinradh/)](https://www.linkedin.com/in/nidhinradh/)
''')
col1.image(app_banner)

configs = {}
code_dir_path = ""
selected_model_type = ""
selected_framework = ""

with st.sidebar:
    st.title(os.environ.get("SIDEBAR_TITLE"))
    st.subheader(os.environ.get("SIDEBAR_TEMPLATE_MENU_SUBHEADING"))

    selected_model_type = st.selectbox(os.environ.get("SIDEBAR_TEMPLATE_MENU_SELECTBOX_LABEL"), set(enabled_templates))
    selected_template_path = os.path.join('./templates', selected_model_type)
    frameworks = [object.name for object in os.scandir(selected_template_path) if (object.is_dir() and object.name in enabled_frameworks)]
    frameworks = sorted(frameworks, key=lambda framework: framework.lower())
    selected_framework = st.selectbox(os.environ.get("SIDEBAR_FRAMEWORK_MENU_SELECTBOX_LABEL"), frameworks, index= 0 if default_framework not in frameworks else frameworks.index(default_framework))
    code_dir_path = os.path.join(selected_template_path, selected_framework)
    config_sidebar = utils.import_from_file(
        "config_sidebar", os.path.join(code_dir_path, "config.py")
    )
    configs = config_sidebar.show()

env = Environment(
    loader=FileSystemLoader(code_dir_path), trim_blocks=True, lstrip_blocks=True,
)

template = env.get_template("code.py.jinja")
code = template.render(header=utils.code_header, notebook=False, **configs)

if(len(code) > 0):
    utils.download_button(code, selected_model_type+"_"+selected_framework+".py", "Download Code")
    st.code(code)













#
#st.sidebar.title(variables.sidebar_title)
#st.sidebar.subheader(variables.sidebar_model_type_subheader)
#selected_model_type = st.sidebar.selectbox(variables.sidebar_model_type_selectbox_label, variables.sidebar_model_type_selectbox_values)

#st.sidebar.subheader(variables.sidebar_pre_processing_subheader)
#is_data_loading =  st.sidebar.checkbox(variables.sidebar_data_loading_checkbox_label, value=True)
#is_normalization =  st.sidebar.checkbox(variables.sidebar_normalization_checkbox_label, value=False)
#is_train_test_split =  st.sidebar.checkbox(variables.sidebar_train_test_split_checkbox_label, value=False)

#st.sidebar.subheader(variables.sidebar_model_subheader)
#selected_model = st.sidebar.selectbox(variables.sidebar_models_selectbox_label, variables.sidebar_models_selectbox_values[selected_model_type])

#st.sidebar.subheader(variables.sidebar_post_processing_subheader)

#st.sidebar.selectbox(variables.sidebar_post_processing_values[selected_model_type]["label"], variables.sidebar_post_processing_values[selected_model_type]["values"])
###
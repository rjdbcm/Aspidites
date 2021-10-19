from dearpygui.dearpygui import *


class GUI(object):
    def __enter__(self, title='Default Viewport', width=800, height=600):
        create_context()
        create_viewport(title=title, width=width, height=height)
        setup_dearpygui()
        # version = get_dearpygui_version()
        # version-specific backwards compatible code can be inserted here for future API changes.

    def __exit__(self, exc_type, exc_val, exc_tb):
        show_viewport()
        start_dearpygui()
        destroy_context()


if __name__ == "__main__":
    with GUI():
        with window(label="Example Window"):
            add_text("Hello world")
            add_input_text(label="string")
            add_slider_float(label="float")

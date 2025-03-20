import dspy
from agent_tools import get_function_list
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

llm = dspy.LM("gemini/gemini-2.0-flash",api_key=os.environ.get("GEMINI_API_KEY"))
dspy.configure(lm=llm)

class AgentDIR(dspy.Signature):
    """Organize text files with categories documented. by managing file operations."""
    input_task = dspy.InputField()
    result = dspy.OutputField(desc="Success message indicating the operation performed.")


class AgentDirUI(App):
    def build(self):
        # Set theme colors
        self.bg_color = get_color_from_hex('#f5f5f5')
        self.accent_color = get_color_from_hex('#2196f3')
        Window.clearcolor = self.bg_color
        
        # Main layout
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Directory selection section - with hint instead of label
        dir_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50)
        self.dir_display = TextInput(
            hint_text='Working Directory',
            readonly=True,
            background_color=get_color_from_hex('#ffffff')
        )
        dir_layout.add_widget(self.dir_display)
        
        browse_button = Button(
            text='Browse',
            size_hint=(0.2, 1),
            background_color=self.accent_color
        )
        browse_button.bind(on_press=self.show_directory_dialog)
        dir_layout.add_widget(browse_button)
        layout.add_widget(dir_layout)
        
        # Task input - with hint instead of label
        self.task_input = TextInput(
            hint_text='Enter task description...',
            multiline=False,
            size_hint=(1, None),
            height=50,
            background_color=get_color_from_hex('#ffffff')
        )
        self.task_input.text = "organize all file in the directory"
        layout.add_widget(self.task_input)

        # Action buttons in a horizontal layout
        action_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50, spacing=10)
        
        self.setup_button = Button(
            text='Setup',
            size_hint=(0.5, 1),
            background_color=self.accent_color
        )
        self.setup_button.bind(on_press=self.setup_agent)
        action_layout.add_widget(self.setup_button)
        
        self.start_button = Button(
            text='Start Agent',
            size_hint=(0.5, 1),
            background_color=self.accent_color
        )
        self.start_button.bind(on_press=self.start_agent)
        action_layout.add_widget(self.start_button)
        
        layout.add_widget(action_layout)
        
        # Results display - minimal label
        layout.add_widget(Label(
            text='Results',
            size_hint=(1, None),
            height=30,
            halign='left',
            text_size=(Window.width, None)
        ))
        
        self.results_display = TextInput(
            readonly=True,
            multiline=True,
            background_color=get_color_from_hex('#ffffff')
        )
        layout.add_widget(self.results_display)
        
        return layout
    
    def show_directory_dialog(self, instance):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.file_chooser = FileChooserListView(path=os.getcwd())
        select_button = Button(
            text='Select',
            size_hint=(1, None),
            height=50,
            background_color=self.accent_color
        )
        select_button.bind(on_press=self.select_directory)
        
        content.add_widget(self.file_chooser)
        content.add_widget(select_button)
        
        from kivy.uix.popup import Popup
        self.popup = Popup(title='Select Directory', content=content, size_hint=(0.9, 0.9))
        self.popup.open()
    
    def select_directory(self, instance):
        self.dir_display.text = self.file_chooser.path
        self.popup.dismiss()

    def setup_agent(self, instance):
        if not self.dir_display.text:
            self.results_display.text = "Please select a working directory first."
            return
        self.selected_path = self.dir_display.text

        # Create directory if it doesn't exist and change to it
        os.makedirs(self.selected_path, exist_ok=True)
        self.original_dir = os.getcwd()
        os.chdir(self.selected_path)
        self.results_display.text = f"Agent setup complete in: {self.selected_path}"
    
    def start_agent(self, instance):
        # Get selected directory
        if not hasattr(self, 'selected_path') or not self.selected_path:
            self.results_display.text = "Please select a working directory first."
            return
        
        # Get task
        task = self.task_input.text
        if not task:
            self.results_display.text = "Please enter a task."
            return

        # Run agent
        try:
            self.results_display.text = "Running agent... Please wait."
            Agent_Module = dspy.ReAct(AgentDIR, tools=get_function_list(), max_iters=20)
            result = Agent_Module(input_task=task)
            self.results_display.text = f"Working directory: {self.selected_path}\n\nTask: {task}\n\nResult:\n{result.result}"
        except Exception as e:
            self.results_display.text = f"Error: {str(e)}"
        finally:
            # Return to original directory
            os.chdir(self.original_dir)


if __name__ == '__main__':
    AgentDirUI().run()
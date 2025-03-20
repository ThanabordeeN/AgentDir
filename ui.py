import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.uix.popup import Popup

# UI Components
class DirectorySelector(BoxLayout):
    """Component for directory selection"""
    def __init__(self, accent_color, **kwargs):
        super().__init__(orientation='horizontal', size_hint=(1, None), height=50, **kwargs)
        self.accent_color = accent_color
        self._build_layout()
        
    def _build_layout(self):
        # Directory input
        self.dir_display = TextInput(
            hint_text='Working Directory',
            readonly=True,
            background_color=get_color_from_hex('#ffffff')
        )
        self.add_widget(self.dir_display)
        
        # Browse button
        browse_button = Button(
            text='Browse',
            size_hint=(0.2, 1),
            background_color=self.accent_color
        )
        browse_button.bind(on_press=self.show_directory_dialog)
        self.add_widget(browse_button)
    
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
        
        self.popup = Popup(title='Select Directory', content=content, size_hint=(0.9, 0.9))
        self.popup.open()
    
    def select_directory(self, instance):
        self.dir_display.text = self.file_chooser.path
        self.popup.dismiss()
        
    def get_selected_path(self):
        return self.dir_display.text

class TaskInput(TextInput):
    """Component for task input"""
    def __init__(self, **kwargs):
        super().__init__(
            hint_text='Enter task description...',
            multiline=False,
            size_hint=(1, None),
            height=50,
            background_color=get_color_from_hex('#ffffff'),
            **kwargs
        )
        self.text = "organize all file in the directory"

class ActionButtons(BoxLayout):
    """Component for action buttons"""
    def __init__(self, accent_color, setup_callback, start_callback, **kwargs):
        super().__init__(orientation='horizontal', size_hint=(1, None), height=50, spacing=10, **kwargs)
        self.accent_color = accent_color
        self._build_layout(setup_callback, start_callback)
        
    def _build_layout(self, setup_callback, start_callback):
        # Setup button
        self.setup_button = Button(
            text='Setup',
            size_hint=(0.5, 1),
            background_color=self.accent_color
        )
        self.setup_button.bind(on_press=setup_callback)
        self.add_widget(self.setup_button)
        
        # Start button
        self.start_button = Button(
            text='Start Agent',
            size_hint=(0.5, 1),
            background_color=self.accent_color
        )
        self.start_button.bind(on_press=start_callback)
        self.add_widget(self.start_button)

class ResultsDisplay(BoxLayout):
    """Component for results display"""
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', size_hint=(1, 1), **kwargs)
        self._build_layout()
        
    def _build_layout(self):
        # Label
        self.add_widget(Label(
            text='Results',
            size_hint=(1, None),
            height=30,
            halign='left',
            text_size=(Window.width, None)
        ))
        
        # Results text area
        self.results_text = TextInput(
            readonly=True,
            multiline=True,
            background_color=get_color_from_hex('#ffffff')
        )
        self.add_widget(self.results_text)
    
    def set_text(self, text):
        self.results_text.text = text
        
    def get_text(self):
        return self.results_text.text

# Main UI App
class AgentDirUI(App):
    def __init__(self, agent_creator, **kwargs):
        super().__init__(**kwargs)
        self.agent_creator = agent_creator
        self.selected_path = None
        self.original_dir = None
        
    def build(self):
        # Theme setup
        self.setup_theme()
        
        # Main layout
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Add components
        self.dir_selector = DirectorySelector(self.accent_color)
        layout.add_widget(self.dir_selector)
        
        self.task_input = TaskInput()
        layout.add_widget(self.task_input)
        
        action_buttons = ActionButtons(
            self.accent_color, 
            self.setup_agent, 
            self.start_agent
        )
        layout.add_widget(action_buttons)
        
        self.results_display = ResultsDisplay()
        layout.add_widget(self.results_display)
        
        return layout
    
    # Theme methods
    def setup_theme(self):
        self.bg_color = get_color_from_hex('#f5f5f5')
        self.accent_color = get_color_from_hex('#2196f3')
        Window.clearcolor = self.bg_color
    
    # Agent operation methods
    def setup_agent(self, instance):
        selected_path = self.dir_selector.get_selected_path()
        if not selected_path:
            self.results_display.set_text("Please select a working directory first.")
            return
        
        self.selected_path = selected_path
        
        # Create directory if it doesn't exist and change to it
        os.makedirs(self.selected_path, exist_ok=True)
        self.original_dir = os.getcwd()
        os.chdir(self.selected_path)
        self.results_display.set_text(f"Agent setup complete in: {self.selected_path}")
    
    def start_agent(self, instance):
        # Get selected directory
        if not self.selected_path:
            self.results_display.set_text("Please select a working directory first.")
            return
        
        # Get task
        task = self.task_input.text
        if not task:
            self.results_display.set_text("Please enter a task.")
            return

        # Run agent
        try:
            self.results_display.set_text("Running agent... Please wait.")
            Agent_Module = self.agent_creator
            result = Agent_Module(input_task=task)
            self.results_display.set_text(
                f"Working directory: {self.selected_path}\n\n"
                f"Task: {task}\n\n"
                f"Result:\n{result.result}"
            )
        except Exception as e:
            self.results_display.set_text(f"Error: {str(e)}")
        finally:
            # Return to original directory
            if self.original_dir:
                os.chdir(self.original_dir)

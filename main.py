from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.lang import Builder


Builder.load_string('''
<SuperGrid>:
    rows: 3
    columns: 3
    spacing: 10
    SuperLabel:
        text: 'R0 C0 RS1 CS1'
        row: 0
        col: 0
    SuperLabel:
        text: 'R2 C1 RS1 CS2'
        row: 2
        col: 1
        colSpan: 2
    SuperLabel:
        text: 'R1 C0 RS2 CS1'
        row: 1
        col: 0
        rowSpan: 2
    SuperLabel:
        text: 'R1 C1 RS1 CS1'
        row: 1
        col: 1
    SuperLabel:
        text: 'R1 C2 RS1 CS1'
        row: 1
        col: 2
    SuperLabel:
        text: 'R0 C1 RS1 CS2'
        row: 0
        col: 1
        colSpan: 2
    
''')

class SuperLabel(Label):
    row = NumericProperty(0)
    col = NumericProperty(0)
    rowSpan = NumericProperty(1)
    colSpan = NumericProperty(1)

    def __init__(self, **kwargs):
        super(SuperLabel, self).__init__(color=(0,0,0,1), **kwargs)

        with self.canvas.before:
            Color(0.9,0.9,1,1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.updateRect, pos=self.updateRect)

    def updateRect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class SuperGrid(FloatLayout):

    rows = NumericProperty(1)
    columns = NumericProperty(1)
    spacing = NumericProperty(0)

    def do_layout(self, *args):
        rows = self.rows
        cols = self.columns
        spacing = self.spacing
        
        for child in self.children:
            
            if not hasattr(child, 'row'):
                child.row = 0
            if not hasattr(child,'col'):
                child.col = 0
            if not hasattr(child, 'rowSpan'):
                child.rowSpan = 1
            if not hasattr(child, 'colSpan'):
                child.colSpan = 1

            row = child.row
            col = child.col
            rowSpan = child.rowSpan
            colSpan = child.colSpan
            
            baseWidth = int((self.width-((cols+1)*spacing))/cols)
            baseHeight = int((self.height-((rows+1)*spacing))/rows)
            
            child.x = (col+1)*spacing + col*baseWidth
            child.y = (row+1)*spacing + row*baseHeight
            
            child.width = baseWidth*colSpan+(colSpan-1)*spacing
            child.height = baseHeight*rowSpan+(rowSpan-1)*spacing
            
        def on_pos(self, *args):
            self.do_layout()

        def on_size(self, *args):
            self.do_layout()

        def add_widget(self, widget):
            super(SuperGrid, self).add_widget(widget)
            self.do_layout()

        def remove_widget(self, widget):
            super(SuperGrid, self).remove_widget(widget)
            self.do_layout()

        

class MyApp(App):
    def build(self):
        return SuperGrid()

MyApp().run()


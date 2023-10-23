#!/usr/bin/env python
# coding: utf-8

# In[1]:


from PyQt5 import uic
from PyQt5.QtGui import QWindow
from RegisterDialog import RegisterDialog


# In[ ]:


class LoginDialog(QWindow):
    """
    The main application window.
    """
    
    def __init__(self):
     
        """
        Load the UI and initialize its components.
        """
        super().__init__()
        self.ui = uic.loadUi('Login_Dialog.ui')
        self.ui.show();
        
        self._Register_Dialog = RegisterDialog()
        
        #self.ui.pushButton.clicked.connect(self.on_Lbutton_click)
        
        self.ui.pushButton_2.clicked.connect(self.on_Rbutton_click)
        


# In[ ]:


    def show_dialog(self):
        self.ui.show()
        
    def on_Rbutton_click(self):
        self.ui=uic.loadUi('Register_Dialog.ui')
        self.ui.show()
        #self._Register_Dialog.show_dialog()
    
    """def on_Lbutton_click(self):
        self._Register_Dialog.show_dialog()"""

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = RegistertDialog()
    form.show_dialog()
    sys.exit(app.exec_())
# In[ ]:





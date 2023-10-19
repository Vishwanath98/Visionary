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
        
        


# In[ ]:


def show_dialog(self):
      """
      Show this dialog.
      """
      self.ui.show()


# In[ ]:





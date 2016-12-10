Shell_enter=[]
vs='vs'
redScore=0
blueScore=0
class Shell(FrontBoard):
    def __init__(self,on_user_msg_recv):
        self.on_user_msg_recv=on_user_msg_recv
        '''
        Create Top
        '''
        self.Shell_top = tk.LabelFrame(self.root)
        self.Shell_top_redscore = tk.Text(self.Shell_top, width=10, height=3)
        self.Shell_top_redscore.grid(row=0, column=0)
        self.Shell_top_redscore.insert(END, "  your\n score\n   {}".format(redScore))
        self.Shell_top_redscore.configure(state='disabled')

        self.Shell_top_vs = tk.Text(self.Shell_top, width=5, height=3,state='disabled')
        self.Shell_top_vs.grid(row=0, column=1)
        self.Shell_top_vs.insert(END, "\n {}".format(vs))


        self.Shell_top_bluescore = tk.Text(self.Shell_top, width=10, height=3)
        self.Shell_top_bluescore.grid(row=0, column=2)
        self.Shell_top_bluescore.insert(END, "opponent's\n  score\n    {}".format(blueScore))
        self.frm_top_bluescore.configure(self.Shell_top_redscore.configure(state='disabled'))


        self.Shell_top_record = tk.Text(self.Shell_top, width=26, height=5, state='disabled')
        self.Shell_top_record.grid(row=1, column=0,columnspan=3)
        self.Shell_top_scroll = tk.Scrollbar(self.Shell_top, orient=VERTICAL,command=self.Shell_top_record.yview)
        self.Shell_top_record['yscrollcommand'] = self.Shell_top_scroll.set
        self.Shell_top_scroll.grid(row=1, column=0, sticky='s' + 'w' + 'e' + 'n',columnspan=3)
        self.Shell_top.grid(row=0, column=0, padx=5, pady=2, sticky='WESN')


        '''
        Create Shell_bottom
        '''
        self.Shell_bottom = tk.LabelFrame(self.root)
        self.Shell_bottom.grid(row=1, column=0, sticky='WESN')
        self.Shell_bottom_sendbox = tk.Text(self.Shell_bottom, width=20, height=7)
        self.Shell_bottom_sendbox.grid(row=0, column=0)

        '''
        Create Buttons
        '''
        self.Shell_buttons = tk.LabelFrame(self.Shell_bottom)
        self.Shell_buttons.grid(row=0, column=1)

        self.Shell_bottom_send = tk.Button(self.Shell_buttons, text='Send', command=self.send)
        self.Shell_bottom_send.grid(row=0, column=0, sticky='WE')

        self.Shell_bottom_surrender = tk.Button(self.Shell_buttons, text='投降', command=FrontBoard.surrender)
        self.Shell_bottom_surrender.grid(row=2, column=0, sticky='EW')

        self.Shell_bottom_withdraw = tk.Button(self.Shell_buttons, text='悔棋', command=FrontBoard.withdraw)
        self.Shell_bottom_withdraw.grid(row=1, column=0, sticky='EW')

    def send(self):
        """
        receive the text content and add it to the record
        """
        self.Shell_top_record.configure(state='normal')
        msg = self.Shell_bottom_sendbox.get(0.0, END)
        self.Shell_top_record.insert(END, "{}".format(msg))
        Shell_enter.append(msg)
        self.Shell_bottom_sendbox.delete(0.0, END)
        self.Shell_top_record.configure(state='disabled')
        self.Shell_top_record.see(END)
    def Shell_print(self,msg):
        self.Shell_top_record.insert(END, "{}".format(msg))


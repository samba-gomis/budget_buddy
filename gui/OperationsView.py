# gui/OperationsView.py
# Assembles the 3 operation tabs: deposit, withdrawal, transfer

import customtkinter as ctk
from gui.operations.Deposit_tab import build_deposit_tab
from gui.operations.Withdrawal_tab import build_withdrawal_tab
from gui.operations.Transfer_tab import build_transfer_tab


class OperationsView(ctk.CTkFrame):

    def __init__(self, parent, account_id: int, on_operation_done=None):
        super().__init__(parent)
        self.account_id        = account_id
        self.on_operation_done = on_operation_done
        self._build_ui()

    def _build_ui(self):
        ctk.CTkLabel(self, text="Operations",
                     font=("Roboto", 20, "bold")).pack(pady=(20, 4))
        ctk.CTkLabel(self, text="Choose an operation below.",
                     font=("Roboto", 12), text_color="gray").pack(pady=(0, 16))

        tabs = ctk.CTkTabview(self)
        tabs.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        tabs.add("Deposit")
        tabs.add("Withdrawal")
        tabs.add("Transfer")

        build_deposit_tab(tabs.tab("Deposit"),
                          self.account_id, self.on_operation_done)
        build_withdrawal_tab(tabs.tab("Withdrawal"),
                             self.account_id, self.on_operation_done)
        build_transfer_tab(tabs.tab("Transfer"),
                           self.account_id, self.on_operation_done)
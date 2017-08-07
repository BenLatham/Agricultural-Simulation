import csvReader.csvReader2 as csv
import itertools
import os
from floss.settings import COSTS_DIR
from simulation.models.accounting_models import Units, Goods, Enterprises, Accounts,\
    AccountsCustomer, AccountsSupplier, AccountsCurrent, AccountsLoans, TradesSheet, Prices

class Admin:
    def __init__(self, scenario, enterprises=None, folder="testing"):
        if enterprises is None:
            self.enterprise_names =["fixed", "dairy", "maize", "forage"]
        else: self.enterprise_names = enterprises
        self.scenario =scenario
        self.folder = os.path.join(COSTS_DIR, folder)


    def setup(self):
        goods, units = self.load_goods()
        self.load_prices()
        enterprises = self.load_enterprises()
        accounts = self.load_accounts()
        self.load_trade_sheets(accounts, enterprises, goods)
        #for enterprise in self.enterprises:
        #    self.read_costs_csv(enterprise, enterprise + "_supplies.csv")


    def load_goods(self):
        data = self.read_goods_csv()
        unique_units = {record[1] for record in data}  # convert to a set so we exclude duplicates
        unit_records = [Units(scenario=self.scenario, name=unit) for unit in unique_units]  # build the records
        units_dict = self.save_get(unit_records, Units)

        goods_records = [Goods(scenario=self.scenario, name=record[0], units=units_dict[record[1]]) for record in data]
        return self.save_get(goods_records, Goods), units_dict


    def load_prices(self):
        data = self.read_prices_file()

    def load_enterprises(self):
        enterprise_records = [Enterprises(scenario=self.scenario, name=enterprise) for enterprise in self.enterprise_names]
        return self.save_get(enterprise_records, Enterprises)

    def load_accounts(self):
        customer = self.read_customer_accounts_file()
        supplier = self.read_supplier_accounts_file()
        current = self.read_current_accounts_file()
        loan = self.read_loans_file()
        accounts = [
            Accounts(scenario=self.scenario, name=row[0], opening_balance=row[1])
            for row in itertools.chain(customer, supplier, current, loan)
            ]

        accounts = self.save_get(accounts, Accounts)
        self.accounts_detail_save(accounts,customer,AccountsCustomer )
        self.accounts_detail_save(accounts,supplier,AccountsSupplier )
        self.accounts_detail_save(accounts,current,AccountsCurrent )
        self.accounts_detail_save(accounts,loan,AccountsLoans )
        return accounts

    def load_trade_sheets(self, accounts, enterprises, goods):
        trade_records =[]
        for enterprise_name, enterprise in enterprises.items():
            data = self.read_supplies_csv(enterprise_name + "_supplies.csv")
            trade_records += self.enterprise_trade_records(data, enterprise, accounts, goods, True)
            data = self.read_supplies_csv(enterprise_name + "_sales.csv")
            trade_records += self.enterprise_trade_records(data, enterprise, accounts, goods, False)
            #enterprise_trade_records()
        self.save_all(trade_records, TradesSheet)

    def enterprise_trade_records(self, data, enterprise, accounts, goods, is_purchase):
        sign = lambda quantity, negative: -quantity if negative else quantity
        return [
            TradesSheet(
                enterprise=enterprise,
                trader=accounts[row[1]],
                item=goods[row[0]],
                month=index + 1,
                quantity=sign(quantity,is_purchase)
            )
            for row in data
            for index, quantity in row
        ]


    def read_goods_csv(self):
        """read the goods file from csv, and return an array of the data"""
        fields = csv.fields([["good"],["units"]])
        return csv.read(self.folder, "goods.csv", fields)


    def read_prices_file(self):
        fields = csv.fields([
            ["item"],
            ["price", "float"],
            ["start","full_date"],
            ["end","full_date"]
        ])
        return csv.read(self.folder, "prices.csv", fields)

    def read_customer_accounts_file(self):
        fields = csv.fields([
            ["name"],
            ["opening balance","float"],
            ["delay","integer"]
        ])
        return csv.read(self.folder, "accounts_customer.csv",fields)

    def read_supplier_accounts_file(self):
        fields = csv.fields([
            ["name"],
            ["opening balance","float"],
            ["credit limit","float"],
            ["interest","float"],
            ["max delay","integer"]
        ])
        return csv.read(self.folder, "accounts_supplier.csv",fields)

    def read_current_accounts_file(self):
        fields = csv.fields([
            ["name"],
            ["opening balance","float"],
            ["overdraft limit","float"],
            ["overdraft interest","float"],
            ["credit interest","float"]
        ])
        return csv.read(self.folder, "accounts_current.csv",fields)

    def read_loans_file(self):
        fields = csv.fields([
            ["name"],
            ["opening balance","float"],
            ["interest","float"],
            ["years to payback","integer"]
        ])
        return csv.read(self.folder, "accounts_loans.csv",fields)


    def read_supplies_csv(self, file):
        fields = csv.fields([
            ["Item"],
            ["supplier"],
            ["Jan", "float"],
            ["Feb", "float"],
            ["Mar", "float"],
            ["Apr", "float"],
            ["May", "float"],
            ["Jun", "float"],
            ["Jul", "float"],
            ["Aug", "float"],
            ["Sep", "float"],
            ["Oct", "float"],
            ["Nov", "float"],
            ["Dec", "float"]
        ])
        return csv.read(self.folder, file, fields)

    def accounts_detail_save(self, accounts_dict, details, account_type):
        account=details[0][0]
        pd = details[0][2]
        account = accounts_dict[account]
        account_records = [account_type(accounts_dict[row[0]].id, *row[2:]) for row in details]
        self.save_all(account_records, account_type)


    def save_get(self, records, model):
        self.save_all(records, model)
        return self.get_all(model)

    def save_all(self, records, model):
        for record in records:
            record.full_clean()  # call full clean on each record
        model.objects.bulk_create(records)  # save to the database


    def get_all(self, model):
        """

        :param model: a database model with fields scenario and name which are unique together
        :return: a dictionary of the fields of the given model corresponding to the current simulation,
         with their name fields as key.
        """
        records = model.objects.filter(scenario=self.scenario)
        return {record.name: record for record in records}







class Connector:
    def __init__(self, db):
        self.db = db
        self.max_id = int(self.db.execute_query('SELECT MAX(exp_id) FROM Expenses')[0][0])

    def changed_expense(self, row, column, exp_id, exp_data):
        # if column == 0:
        #     query = None
        #     return 'нельзя менять id'
        if column == 1:
            data = float(exp_data)
            query = '''UPDATE Expenses SET date = ? WHERE exp_id = ?'''
        elif column == 2:
            data = float(exp_data)
            query = '''UPDATE Expenses SET sum = ? WHERE exp_id = ?'''
        elif column == 3:
            data = exp_data
            query = '''UPDATE Expenses SET cat = ? WHERE exp_id = ?'''
        elif column == 4:
            data = exp_data
            query = '''UPDATE Expenses SET comm = ? WHERE exp_id = ?'''
        params = (data, int(exp_id))
        print(params)
        self.db.execute_query(query, params)
        print(self.db.execute_query('SELECT * FROM Expenses'))

    def add_expense(self, new_exp):
        print(new_exp)
        query = 'INSERT INTO Expenses(exp_id, date, sum, cat, comm) VALUES (?,?,?,?,?)'
        new_id = self.max_id + 1
        self.max_id+=1
        params = (new_id, int(new_exp[0]), float(new_exp[1]), new_exp[2], new_exp[3])
        self.db.execute_query(query, params)


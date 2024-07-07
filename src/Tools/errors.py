class errors:
    def __init__(self, row, column, message, errorType):
        self.row = row
        self.column = column
        self.message = message
        self.errorType = errorType
        pass

    def printError(self):
        truncated_message = self.message[:80] + "..." if len(self.message) > 50 else self.message
        message = f"{truncated_message} | Error Type: {self.errorType}"
        if self.row != 0:
            message.append(f" | Row: {self.row}")
            if self.column != 0:
                message.append(f", Column: {self.column}")
        elif self.column != 0:
            message.append(f" | Column: {self.column}")
            
        print(message)

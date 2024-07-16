class Errors:
    def __init__(self, row, column, message, errorType):
        self.row = row
        self.column = column
        self.message = message
        self.errorType = errorType

    def printError(self):
        truncated_message = self.message + "..." if len(self.message) > 50 else self.message
        message = f"{truncated_message} | Error Type: {self.errorType}"
        if self.row != 0:
            message+=(f" | Row: {self.row}")
            if self.column != 0:
                message+=(f", Column: {self.column}")
        elif self.column != 0:
            message+=(f" | Column: {self.column}")
            
        print(message)

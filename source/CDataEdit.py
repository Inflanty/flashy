from CDataView import DataView

class DataEdit(DataView) :
    __editItemsUpdate = DataView.itemsUpdated
    __editItemsDeleted = DataView.itemsDeleted
    def getEdited(self) :
        for row in self.__editItemsUpdate :
            for index in range(len(DataView.itemsDeleted)) :
                if DataView.itemsDeleted[index] in row[0] :
                    self.__editItemsUpdate.remove(row)
        return self.__editItemsUpdate

    def getDeleted(self) :
        return self.__editItemsDeleted

    def getNew(self) :
        pass
    
    ## Here we have to return data
    #  TOBEDECIDED :
    #   - how to sign data of Edited
    #   - how to sign data of Deleted
    #   - how to sign data of New
    def pull(self) :
        pass

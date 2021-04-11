from CDataView import DataView

class DataNew(DataView) :
    __newItemsDeleted = DataView.itemsDeleted
    def getEdited(self) :
        self.__newItemsUpdate = DataView.itemsUpdated
        self.pull()
        # Check the difference between __newItemsUpdate AND DataView.itemsUpdated
        # if some elements are different, we should take newest version
        return DataView.itemsUpdated

    def getDeleted(self) :
        return None

    ## Remove row from view and store deleted ID
    def rmRow(self) :
        _row = self.selectedRow() + 1
        if _row != None :
            logging.info('Remove row : ' + str(_row))
            self.table.removeRow(_row - 1)
        else :
            logging.info('Select row to delete!')

    ## Update current list of elements
    def pull(self) :
        _rowContent = []
        for _row in range(self.table.rowCount) :
            for _columns in range(self.columnCount) :
                _singleitem = self.table.item(_row, _columns).text()
                _rowContent.append(_singleitem)
            self.__updateMyItems(self.__mapViewToDbFormat(_rowContent))
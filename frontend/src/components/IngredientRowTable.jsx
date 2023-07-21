import { forwardRef, useImperativeHandle, useState } from 'react';
import PropTypes from 'prop-types';
import { Table, TableBody, TableCell, TableRow, TextField, IconButton } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import SelectDropdown from './SelectDropdown';

// eslint-disable-next-line react/display-name
const RowTable = forwardRef((props, _ref) => {
  const [rows, setRows] = useState([[]]);
  const columnsArray = ['Ingredient', 'Amount'];

  useImperativeHandle(_ref, () => ({
    getRows: () => {
      return rows;
    },
  }));

  const handleAddRow = () => {
    setRows([...rows, []]);
  };

  const handleRemoveRow = (idx) => {
    const tempRows = [...rows]; // avoid state mutation
    tempRows.splice(idx, 1);
    setRows(tempRows);
  };

  const updateState = (e, row, col) => {
    const value = e.target.value;
    const rowsCopy = rows;
    rowsCopy[row][col] = value;
    setRows(rowsCopy);
  };

  return (
    <Table sx={{ minWidth: 300 }} aria-label="simple table">
      <TableBody>
        {rows.map((item, row) => (
          <TableRow key={row}>
            {/* {columnsArray.map((column, col) => (
              <TableCell key={col}>
                <TextField
                  required
                  id={`${column}${row}_${col}`}
                  label={column}
                  value={rows[row][col]}
                  onChange={(e) => updateState(e, row, col)}
                  variant="standard"
                />
              </TableCell>
            ))} */}
            <TableCell key={0}>
              <SelectDropdown
                id={`${columnsArray[0]}${row}_0`}
                label="Ingredient"
                items={props.ingredients}
                showNone={false}
                onChange={(event) => updateState(event, row, 0)}
              />
            </TableCell>
            <TableCell key={1}>
              <TextField
                required
                id={`${columnsArray[1]}${row}_1`}
                onChange={(e) => updateState(e, row, 1)}
                variant="standard"
              />
            </TableCell>

            <TableCell padding="none" size="small">
              <IconButton onClick={() => handleRemoveRow(row)} disabled={rows.length === 1}>
                <DeleteIcon />
              </IconButton>
              <IconButton onClick={handleAddRow}>
                <AddIcon />
              </IconButton>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
});

RowTable.propTypes = {
  ingredients: PropTypes.object,
};

export default RowTable;

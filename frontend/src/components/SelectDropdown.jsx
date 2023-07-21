import { useEffect, useState } from 'react';
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import PropTypes from 'prop-types';

const BasicSelect = (props) => {
  const [value, setValue] = useState(props.value || '');

  const handleChange = (event) => {
    setValue(event.target.value);
    props.onChange(event);
  };

  useEffect(() => {
    if (props.disabled) {
      setValue('');
    }
  }, [props.disabled]);

  return (
    <Box sx={{ minWidth: 120 }}>
      <FormControl fullWidth disabled={props.disabled}>
        <InputLabel>{props.label}</InputLabel>
        <Select id={props.id} value={value} label={props.label} onChange={handleChange}>
          {props.showNone && (
            <MenuItem value="">
              <em>None</em>
            </MenuItem>
          )}
          {!!props.items &&
            Object.entries(props.items).map(([key, val]) => {
              return (
                <MenuItem
                  key={key}
                  value={key}
                  disabled={props.itemDisabled != null ? props.itemDisabled(key) : false}
                >
                  {val.name}
                </MenuItem>
              );
            })}
        </Select>
      </FormControl>
    </Box>
  );
};

BasicSelect.propTypes = {
  id: PropTypes.string,
  label: PropTypes.string,
  items: PropTypes.object,
  disabled: PropTypes.bool,
  onChange: PropTypes.func,
  itemDisabled: PropTypes.func,
  showNone: PropTypes.bool,
  value: PropTypes.string,
};

export default BasicSelect;

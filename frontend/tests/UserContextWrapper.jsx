import { UserContext } from '../src/App';
import PropTypes from 'prop-types';

const UserContextWrapper = (props) => {
  return <UserContext.Provider value={{ user: props.user }}>{props.child}</UserContext.Provider>;
};

UserContextWrapper.propTypes = {
  child: PropTypes.any,
  user: PropTypes.object,
};

export default UserContextWrapper;

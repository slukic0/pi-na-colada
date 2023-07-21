import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it, vi } from 'vitest';
import CreateIngredient from '../src/components/CreateIngredient';
import axios from 'axios';

//import { mock } from '@testing-library/react';

vi.mock('axios');

describe('create ingredient', () => {
  it('should render and submit a POST request', async () => {
    const user = userEvent.setup();
    render(<CreateIngredient />);

    //screen.getByRole('textbox');

    const name = screen.getByRole('textbox', {
      name: /name/i,
    });
    const description = screen.getByRole('textbox', {
      name: /description/i,
    });
    const createBtn = screen.getByRole('button', {
      name: /create/i,
    });

    await user.clear(name);
    await user.type(name, 'testName');

    await user.clear(description);
    await user.type(description, 'testDesc');

    await user.click(createBtn);

    expect(axios.post.mock.calls[0][1]).toMatchObject({
      description: 'testDesc',
      name: 'testName',
    });
  });

  it('should match its snapshot', () => {
    const tree = render(<CreateIngredient />);
    expect(tree).toMatchSnapshot();
  });
});

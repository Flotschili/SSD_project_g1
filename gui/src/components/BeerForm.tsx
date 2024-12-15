import React, { useState, useEffect } from 'react';
import { TextField, Button, Dialog, DialogTitle, DialogContent, DialogActions } from '@mui/material';
import { Beer } from '../models/Beer';
import BeerService from '../services/BeerService';
import { set } from 'react-hook-form';

interface BeerFormProps {
  open: boolean;
  onClose: () => void;
  beer?: Beer | null;
  onSave: () => void;
}

const BeerForm: React.FC<BeerFormProps> = ({ open, onClose, beer, onSave }) => {
  const [formBeer, setFormBeer] = useState<Partial<Beer>>({ name: '', brewery: '', description: '', alcohol_content: 0 });
  const [errors, setErrors] = useState<{ [key: string]: string[] }>({});

  useEffect(() => {
    if (beer) {
      setFormBeer(beer);
    } else {
      setFormBeer({ name: '', brewery: '', description: '', alcohol_content: 0 });
    }
  }, [beer]);

  const handleSave = () => {
    let promise;
    if (beer) {
      promise = BeerService.updateBeer(formBeer.id!!, formBeer as Beer);
    } else {
      promise = BeerService.createBeer(formBeer as Beer);
    }

    promise
      .then(() => {
        setErrors({});
		setFormBeer({ name: '', brewery: '', description: '', alcohol_content: 0 });
        onSave();
        onClose();
      })
      .catch((err) => {
        if (err.response.status === 400) {
          setErrors(err.response.data);
        } else {
          alert("Failed to save beer: " + err);
        }
      });
  };

  return (
    <Dialog open={open} onClose={onClose}>
      <DialogTitle>{beer ? "Edit Beer" : "Add Beer"}</DialogTitle>
      <DialogContent>
        <TextField
          label="Name"
          value={formBeer.name}
          onChange={(e) => setFormBeer({ ...formBeer, name: e.target.value })}
          fullWidth
          margin="normal"
          error={!!errors.name}
          helperText={errors.name ? errors.name.join(', ') : ''}
        />
        <TextField
          label="Brewery"
          value={formBeer.brewery}
          onChange={(e) =>
            setFormBeer({ ...formBeer, brewery: e.target.value })
          }
          fullWidth
          margin="normal"
          error={!!errors.brewery}
          helperText={errors.brewery ? errors.brewery.join(', ') : ''}
        />
        <TextField
          label="Description"
          value={formBeer.description}
          onChange={(e) =>
            setFormBeer({ ...formBeer, description: e.target.value })
          }
          fullWidth
          margin="normal"
          multiline
          rows={4}
          error={!!errors.description}
          helperText={errors.description ? errors.description.join(', ') : ''}
        />
        <TextField
          label="Alcohol Percent"
		  type='number'
          value={formBeer.alcohol_content}
          onChange={(e) =>
            setFormBeer({ ...formBeer, alcohol_content: parseFloat(e.target.value) })
          }
          fullWidth
          margin="normal"
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} color="primary">
          Cancel
        </Button>
        <Button onClick={handleSave} color="primary">
          {beer ? 'Save' : 'Add'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default BeerForm;
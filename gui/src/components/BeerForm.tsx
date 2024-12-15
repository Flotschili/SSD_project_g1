import React, { useState, useEffect } from "react";
import {
  TextField,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  Select,
  InputLabel,
  MenuItem,
  DialogContentText,
} from "@mui/material";
import { Beer, BeerType } from "../models/Beer";
import BeerService from "../services/BeerService";
import { set } from "react-hook-form";

interface BeerFormProps {
  open: boolean;
  onClose: () => void;
  beer?: Beer | null;
  onSave: () => void;
}

const DEFAULT_BEER: Partial<Beer> = {
	  name: "",
  beer_type: BeerType.PaleLager,
  brewery: "",
  description: "",
  alcohol_content: 0,
};

const BeerForm: React.FC<BeerFormProps> = ({ open, onClose, beer, onSave }) => {
  const [formBeer, setFormBeer] = useState<Partial<Beer>>(DEFAULT_BEER);
  const [errors, setErrors] = useState<{ [key: string]: string[] }>({});
  const [confirmOpen, setConfirmOpen] = useState(false);

  useEffect(() => {
    if (beer) {
      setFormBeer(beer);
    }
  }, [beer]);

  const handleDeleteClick = () => {
    setConfirmOpen(true);
  };

  const handleConfirmClose = () => {
    setConfirmOpen(false);
  };

  const handleConfirmDelete = () => {
    setConfirmOpen(false);
    handleDelete();
  };

  const handleDelete = () => {
	if (beer) {
	  BeerService.deleteBeer(beer.id)
		.then(() => {
		  onClose();
		  onSave();
		})
		.catch((err) => {
		  alert("Failed to delete beer: " + err);
		});
	}
  }


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
        setFormBeer(DEFAULT_BEER);
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
          helperText={errors.name ? errors.name.join(", ") : ""}
        />
        <FormControl fullWidth margin="normal" error={!!errors.beer_type}>
          <InputLabel>Beer Type</InputLabel>
          <Select
            value={formBeer.beer_type}
            onChange={(e) =>
              setFormBeer({
                ...formBeer,
                beer_type: e.target.value as BeerType,
              })
            }
          >
            {Object.values(BeerType).map((type) => (
              <MenuItem key={type} value={type}>
                {type}
              </MenuItem>
            ))}
          </Select>
          {errors.beer_type && (
            <p style={{ color: "red" }}>{errors.beer_type.join(", ")}</p>
          )}
        </FormControl>
        <TextField
          label="Brewery"
          value={formBeer.brewery}
          onChange={(e) =>
            setFormBeer({ ...formBeer, brewery: e.target.value })
          }
          fullWidth
          margin="normal"
          error={!!errors.brewery}
          helperText={errors.brewery ? errors.brewery.join(", ") : ""}
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
          helperText={errors.description ? errors.description.join(", ") : ""}
        />
        <TextField
          label="Alcohol Percent"
          type="number"
          value={formBeer.alcohol_content}
          onChange={(e) =>
            setFormBeer({
              ...formBeer,
              alcohol_content: parseFloat(e.target.value),
            })
          }
          fullWidth
          margin="normal"
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={handleDeleteClick} color="warning">
          Delete
        </Button>
		<Button onClick={onClose} color="primary">
          Cancel
        </Button>
        <Button onClick={handleSave} color="primary">
          {beer ? "Save" : "Add"}
        </Button>
      </DialogActions>
	  <Dialog
        open={confirmOpen}
        onClose={handleConfirmClose}
      >
        <DialogTitle>Confirm Delete</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Are you sure you want to delete this beer?
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleConfirmClose} color="primary">
            Cancel
          </Button>
          <Button onClick={handleConfirmDelete} color="secondary">
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </Dialog>
  );
};

export default BeerForm;

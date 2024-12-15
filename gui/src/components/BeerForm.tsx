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

const MAX_NAME_LENGTH = 100;
const MAX_BREWERY_LENGTH = 100;
const MAX_DESCRIPTION_LENGTH = 1000;
const MIN_ALCOHOL_CONTENT = 0;
const MAX_ALCOHOL_CONTENT = 75;

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

  const validate = () => {
    const newErrors: { [key: string]: string[] } = {};

    if (!formBeer.name || formBeer.name.trim() === "") {
      newErrors.name = ["Name must not be empty."];
    } else if (!/^[A-Z]/.test(formBeer.name)) {
      newErrors.name = ["Name must start with a capital letter."];
    } else if (formBeer.name.length > MAX_NAME_LENGTH) {
      newErrors.name = [`Name must not exceed ${MAX_NAME_LENGTH} characters.`];
    } else if (!/^[a-zA-Z\s]*$/.test(formBeer.name)) {
      newErrors.name = ["Name must not contain special characters."];
    }

    if (!formBeer.brewery || formBeer.brewery.trim() === "") {
      newErrors.brewery = ["Brewery name must not be empty."];
    } else if (!/^[A-Z]/.test(formBeer.brewery)) {
      newErrors.brewery = ["Brewery name must start with a capital letter."];
    } else if (formBeer.brewery.length > MAX_BREWERY_LENGTH) {
      newErrors.brewery = [
        `Brewery name must not exceed ${MAX_BREWERY_LENGTH} characters.`,
      ];
    } else if (!/^[a-zA-Z\s]*$/.test(formBeer.brewery)) {
      newErrors.brewery = ["Brewery name must not contain special characters."];
    }

    if (
      formBeer.description &&
      formBeer.description.length > MAX_DESCRIPTION_LENGTH
    ) {
      newErrors.description = [
        `Description must not exceed ${MAX_DESCRIPTION_LENGTH} characters.`,
      ];
    }

    if (
      formBeer.beer_type !== BeerType.NonAlcoholicBeer &&
      formBeer.beer_type !== BeerType.AlcoholFreeWheatBeer &&
      formBeer.beer_type !== BeerType.AlcoholFreeLager &&
      (!formBeer.alcohol_content ||
        formBeer.alcohol_content < MIN_ALCOHOL_CONTENT ||
        formBeer.alcohol_content > MAX_ALCOHOL_CONTENT)
    ) {
      newErrors.alcohol_content = [
        `Alcohol content must be between ${MIN_ALCOHOL_CONTENT} and ${MAX_ALCOHOL_CONTENT} % ABV.`,
      ];
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

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
  };

  const handleSave = () => {
    if (!validate()) {
      return;
    }

    let promise;
    if (beer) {
      promise = BeerService.updateBeer(formBeer.id!!, formBeer as Beer);
    } else {
      promise = BeerService.createBeer(formBeer as Beer);
    }

    promise
      .then(() => {
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
                alcohol_content:
                  formBeer?.beer_type === BeerType.NonAlcoholicBeer ||
                  formBeer?.beer_type === BeerType.AlcoholFreeWheatBeer ||
                  formBeer?.beer_type === BeerType.AlcoholFreeLager
                    ? 0
                    : formBeer.alcohol_content,
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
        {formBeer.beer_type === BeerType.NonAlcoholicBeer ||
        formBeer.beer_type === BeerType.AlcoholFreeWheatBeer ||
        formBeer.beer_type === BeerType.AlcoholFreeLager ? null : (
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
            error={!!errors.alcohol_content}
            helperText={
              errors.alcohol_content ? errors.alcohol_content.join(", ") : ""
            }
            fullWidth
            margin="normal"
          />
        )}
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
      <Dialog open={confirmOpen} onClose={handleConfirmClose}>
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

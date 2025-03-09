import { Box, Button, Dialog, DialogActions, DialogContent, DialogTitle, Grid, Grid2, Typography } from "@mui/material";
import { Switch } from "pretty-checkbox-react";

const MovieDialog = ({ movie, onClose, open, handleMarkForDownload }) => {
    return (
        open && (
            <>
                <Dialog open={open} onClose={onClose} fullWidth maxWidth="lg">
                    <DialogTitle>{movie.title}</DialogTitle>
                    <DialogContent>
                        <Grid container item direction='row' xs={12}>
                            <Grid item xs={6}>
                                <img src={movie?.large_cover_image} alt={movie.title} />
                            </Grid>
                            <Grid item xs={6}>
                                <Typography variant="h4">{movie.title}</Typography>
                                <Typography variant="h6">{movie.year}</Typography>
                                <Typography variant="h6">{movie.rating.toFixed(1)}</Typography>
                                <Typography variant="body1">{movie.description_full}</Typography>
                                <Switch shape="slim" color="success" checked={movie.mark_for_download} onChange={(ev) => handleMarkForDownload && handleMarkForDownload(movie.id,ev.target.checked )}>{movie.mark_for_download ? 'Marcada para descarga' : 'Marcar para descarga'}</Switch>
                            </Grid>
                        </Grid>
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={onClose} color="primary">
                            Cerrar
                        </Button>
                    </DialogActions>
                </Dialog>
            </>
        )
    )
}
export default MovieDialog;
import { Box, Button, Card, CardContent, CardMedia,  Grid2, Hidden, Typography } from "@mui/material";
import { motion } from "framer-motion";
import { Checkbox, Switch } from 'pretty-checkbox-react';
import '@djthoms/pretty-checkbox';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import { green } from "@mui/material/colors";

const MovieCard = ({ movie, handleMarkForDownload, onClick }) => {
    return (
        <Grid2 item xs={12} sm={6} md={4} key={movie.id} onClick={() => onClick && onClick(movie)}>
            <motion.div
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
            >
                <Box sx={{ display: 'flex', justifyContent: 'center', position: 'relative', cursor: 'pointer' }} >
                {movie.mark_for_download && <CheckCircleIcon style={{position:'absolute', color:green[600], top:10, right:10 }} />
                        }
                    <img src={movie.medium_cover_image} alt={movie.title} style={{ maxWidth: 200 }} />

                    <Box style={{
                        position: 'absolute',
                        bottom: 0,
                        width: '100%',
                        backgroundColor: 'rgba(0, 0, 0, 0.5)',
                        color: 'white',
                        padding: 2,
                        textAlign: 'center',
                        height: 50, margin: 2

                    }}>
                        
                        <Box display={'flex'} flexDirection={'row'} justifyContent={'center'} alignItems={'center'}>
                            <Typography variant="h6" style={{ flexGrow: 1 }} noWrap>{movie.title}</Typography>

                            <Typography variant="body" style={{ margin: 5, fontSize: 12 }} >{movie.rating.toFixed(1)}</Typography>

                        </Box>
                        <Box display={'flex'} flexDirection={'row'} justifyContent={'center'} alignItems={'center'}>
                            <Typography variant="body" style={{ margin: 5, fontSize: 12 }} >{movie.year}</Typography>
                            
                        </Box>
                    </Box>
                </Box>
            </motion.div>
            {/* <Card style={{ maxWidth: 200, height: 500 }}>
                <CardMedia component='img' image={movie.medium_cover_image} style={{ maxWidth: 200 }} />
                <CardContent>
                    <Typography variant="h6">{movie.title}</Typography>
                    <Typography variant="body2" color="text.secondary">{movie.description}</Typography>
                    <Button
                        variant="contained"
                        color={movie.mark_for_download ? 'success' : 'primary'}
                        onClick={() => handleMarkForDownload(movie.id)}
                        sx={{ mt: 2 }}
                    >
                        {movie.mark_for_download ? 'Marcada para descarga' : 'Marcar para descarga'}
                    </Button>
                </CardContent>
            </Card> */}
        </Grid2>
    )
};

export default MovieCard;


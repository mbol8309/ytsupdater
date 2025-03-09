import React, { useMemo, useState } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import instance from './api';
import { Container, Grid2, TextField, Button, Card, CardContent, Typography, CardMedia, Autocomplete, Checkbox, FormLabel, Grid } from '@mui/material';
import ResponsivePagination from 'react-responsive-pagination';
import 'react-responsive-pagination/themes/classic.css';
import { Controller, useForm } from "react-hook-form"
import MovieCard from './MovieCard';
import MovieDialog from './MovieDialog';

const fetchMovies = async (filters = {}) => {
    const { data } = await instance.get('/movies', {
        params: Object.keys(filters)
            .reduce((p, c) => {
                if (filters[c] !== undefined && filters[c] !== '') {
                    p[c] = filters[c];
                }
                return p;
            }, {})
    });
    return data;
};


const fetchGenres = async (filters) => {
    const { data } = await instance.get('/genres', {
        params: Object.keys(filters)
            .reduce((p, c) => {
                if (filters[c] !== undefined && filters[c] !== '') {
                    p[c] = filters[c];
                }
                return p;
            }, {})
    });
    return data;
};

const updateMovie = async (movieId, data) => {
    const response = await instance.patch(`/movies/${movieId}/mark`, data);
    return response.data;
};

const MovieList = () => {
    const [currentPage, setCurrentPage] = useState(1);
    const {
        handleSubmit,
        control,
    } = useForm({
        defaultValues: {
            title: '',
            genre: '',
            rating: 1,
            per_page: 50,
            marked: undefined
        }
    })

    const [filters, setFilters] = useState({ title: '', genre: '', rating: '', per_page: 20 });
    const filtersTotal = useMemo(() => {
        return { ...filters, page: currentPage };
    }, [filters, currentPage]);

    const { data: movies, error, isLoading } = useQuery(['movies', filtersTotal], () => fetchMovies(filtersTotal), {
        placeholderData: [],
    });

    const [Genresfilters, setGenreFilters] = useState({ title: '', per_page: 50 });

    const totalPages = useMemo(() => movies.total_pages, [movies]);



    const { data: genres } = useQuery(['genres', Genresfilters], () => fetchGenres(Genresfilters), {
        select: (data) => data.items,
        placeholderData: [],
    });
    const mutation = useMutation(({movieId,value}) => updateMovie(movieId, { mark_for_download: value }),);
    const queryClient = useQueryClient();
    // const handleFilterChange = (e) => {
    //     const { name, value } = e.target;
    //     setFilters((prevFilters) => ({ ...prevFilters, [name]: value }));
    //     setCurrentPage(1);

    // };

    const handleMarkForDownload = (movieId, value) => {
        console.log(value)
        mutation.mutate({movieId, value}, {
            onSuccess: (data) => {
                if (selectedMovie != null && selectedMovie.id === movieId) {
                    setSelectedMovie((movie) => ({ ...movie, ...data }));
                }
                queryClient.setQueryData(['items'], (oldData) => {
                    if (!oldData) return [];
              
                    return oldData.map((item) =>
                      item.id === data.id ? data : item
                    );
                  });
            }
        });
    };


    const onSubmit = (data) => {
        console.log(data)
        setFilters((filters) => ({ ...filters, ...data }));
        setCurrentPage(1);
    }

    const [selectedMovie, setSelectedMovie] = useState(null);


    if (isLoading) return <div>Cargando...</div>;
    if (error) return <div>Error al cargar las películas</div>;


    return (
        <Container>
            <Grid container style={{margin:5}}>
            <Grid item xs={12}>
                <ResponsivePagination
                    current={currentPage}
                    total={totalPages}
                    onPageChange={setCurrentPage}
                    />
                    </Grid>
            </Grid>
            <form onSubmit={handleSubmit(onSubmit)}>
                <Grid2 container gap={1} style={{ margin: 20 }}>
                    <Grid2 item sm={4}>
                        <Controller
                            control={control}
                            name='title'
                            render={({ field }) => (
                                <TextField
                                    {...field}
                                    fullWidth
                                    label="Filtrar por título"
                                />
                            )} />
                    </Grid2>
                    <Grid2 item xs={12}>
                        <Controller
                            control={control}
                            name='genre'
                            render={({ field }) => (
                                <Autocomplete
                                    {...field}
                                    options={genres ?? []}
                                    getOptionLabel={(option) => option.title ?? ""}
                                    getOptionKey={(option) => option.title ?? ""}
                                    fullWidth
                                    onInputChange={(ev, value) => setGenreFilters((filters) => ({ ...filters, title: value ?? "" }))}
                                    renderInput={(params) => (
                                        <TextField fullWidth {...params} label="Selecciona una película" variant="outlined" />
                                    )}
                                    onChange={(e, value) => field.onChange(value?.title)}
                                    label="Filtrar por género"
                                />
                            )} />
                    </Grid2>

                    <Grid2 item >
                        <Controller
                            control={control}
                            name='rating'
                            rules={{ min: 1, max: 10 }}
                            render={({ field }) => (
                                <TextField
                                    {...field}
                                    aria-valuemax={10}
                                    aria-valuemin={1}
                                    fullWidth
                                    label="Filtrar por calificación"
                                    type="number"
                                    
                                />)} />
                    </Grid2>
                    {/* <Grid2 item xs={12}>
                        <Controller
                            control={control}
                            name='marked'
                            render={({ field }) => (
                                // <>
                                //     <FormLabel >Marcados para descarga</FormLabel>
                                    <Checkbox {...field} onChange={(ev)=>field.onChange(ev.target.value)} label="Filtrar por marcadas para descarga" />
                                    // </>
                            )} />
                    </Grid2> */}
                    <input type='submit' style={{ display: 'none' }} />

                </Grid2>
            </form>
            <Grid2 container spacing={2}>
                {movies?.items?.map((movie) => (
                    <MovieCard movie={movie} key={movie.id} handleMarkForDownload={handleMarkForDownload} onClick={(movie) => setSelectedMovie(movie)} />
                ))}
            </Grid2>
            <Grid container style={{margin:5}}>
            <Grid item xs={12}>
                <ResponsivePagination
                    current={currentPage}
                    total={totalPages}
                    onPageChange={setCurrentPage}
                    />
                    </Grid>
            </Grid>
            <MovieDialog movie={selectedMovie} onClose={() => setSelectedMovie(null)} open={selectedMovie !== null} handleMarkForDownload={handleMarkForDownload} />

        </Container>
    );
};

export default MovieList;

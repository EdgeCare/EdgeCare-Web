import React from 'react';
import { Box, Typography, TextField, Button, CircularProgress } from '@mui/material';

interface InputPanelProps {
    inputText: string;
    loading: boolean;
    onInputChange: (e: React.ChangeEvent<HTMLTextAreaElement>) => void;
    onSubmit: () => void;
}

const InputPanel: React.FC<InputPanelProps> = ({ inputText, loading, onInputChange, onSubmit }) => {
    return (
        <Box sx={{ p: 2, borderRight: { md: '2px solid #ccc' }, backgroundColor: '#ffffff' }}>
            <Typography variant="h5" sx={{ mb: 2 }}>
                🖊️ Raw Medical Note
            </Typography>

            <TextField
                multiline
                rows={20}
                variant="outlined"
                placeholder="Paste your medical note here..."
                fullWidth
                value={inputText}
                onChange={onInputChange}
                sx={{ mb: 2, backgroundColor: '#f5f5f5', borderRadius: '5px' }}
            />

            <Button
                variant="contained"
                color="primary"
                fullWidth
                onClick={onSubmit}
                disabled={loading}
            >
                {loading ? <CircularProgress size={24} /> : '🔍 Analyze'}
            </Button>
        </Box>
    );
};

export default InputPanel;

import React, { useState } from 'react';
import { Box } from '@mui/material';
import axios from 'axios';
import InputPanel from './components/InputPanel';
import OutputPanel from './components/OutputPanel';

// Interface for prediction results
interface Token {
    token: string;
    tag: string;
}

function App() {
    const [inputText, setInputText] = useState('');
    const [output, setOutput] = useState<Token[]>([]);
    const [loading, setLoading] = useState(false);

    // Handle text input changes
    const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setInputText(e.target.value);
    };

    // Submit text to the server for inference
    const handleSubmit = async () => {
        if (!inputText) return;

        setLoading(true);
        
        try {
            const response = await axios.post('http://localhost:8000/predict', { text: inputText });
            setOutput(response.data.results);
        } catch (error) {
            console.error('Error during prediction:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <Box
        sx={{
            height: '100vh',
            display: 'grid',
            gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' },
            gridTemplateRows: '1fr',
            gap: 2,
        }}
        >
            {/* Input Component */}
            <InputPanel
                inputText={inputText}
                loading={loading}
                onInputChange={handleInputChange}
                onSubmit={handleSubmit}
            />

            {/* Output Component */}
            <OutputPanel output={output} />
        </Box>
    );
}

export default App;

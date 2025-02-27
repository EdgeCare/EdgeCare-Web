import React from 'react';
import { Box, Typography } from '@mui/material';

interface Token {
    token: string;
    tag: string;
}

interface OutputPanelProps {
    output: Token[];
}

const OutputPanel: React.FC<OutputPanelProps> = ({ output }) => {
    // Assign colors to tags for better visualization
    const getTagColor = (tag: string) => {
        switch (tag) {
            case 'PERSON':
                return '#FF6B6B'; // Red
            case 'LOC':
                return '#6BCB77'; // Green
            case 'AGE':
                return '#FFD93D'; // Yellow
            case 'PHONE':
                return '#4D96FF'; // Blue
            case 'EMAIL':
                return '#845EC2'; // Purple
            case 'HOSPITAL':
                return '#E07C24'; // Orange
            case 'DATE':
                return '#D65DB1'; // Pink
            case 'STAFF':
                return '#FF9671'; // Peach
            case 'URL':
                return '#00C9A7'; // Aqua
            case 'TIMESTAMPS':
                return '#FFD700'; // Gold
            default:
                return '#A0A0A0'; // Gray for unknown tags
        }
    };

    return (
        <Box sx={{ p: 2, backgroundColor: '#f9fafc' }}>
            <Typography variant="h5" sx={{ mb: 2 }}>
                🏷️ Anonymized Medical Note
            </Typography>
            <Box
                sx={{
                    height: '90%',
                    overflowY: 'auto',
                    whiteSpace: 'pre-wrap',
                    backgroundColor: '#ffffff',
                    p: 2,
                    borderRadius: '5px',
                }}
            >
                {output.length > 0 ? (
                    output.map((item, index) => (
                        item.tag === 'O' ? (
                            item.token === '\n' ? (
                                <span key={index} style={{ margin: '2px' }}>
                                    {item.token}
                                </span>
                            ) : (
                                <span key={index} style={{ margin: '2px' }}>
                                    {item.token + ' '}
                                </span>
                            )
                        ) : (
                            // Render highlighted tokens for other tags
                            <span
                                key={index}
                                style={{
                                    backgroundColor: getTagColor(item.tag),
                                    color: '#fff',
                                    borderRadius: '5px',
                                    padding: '4px 6px',
                                    margin: '2px',
                                    display: 'inline-block',
                                    fontSize: '14px',
                                }}
                            >
                                {item.token} <small>({item.tag})</small>
                            </span>
                        )
                    ))
                ) : (
                    <Typography color="text.secondary">No predictions yet.</Typography>
                )}
            </Box>
        </Box>
    );
};

export default OutputPanel;

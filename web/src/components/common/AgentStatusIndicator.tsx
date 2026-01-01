/**
 * Agent Status Indicator Component
 * Shows the current status of the AI agent
 */

import { Chip, CircularProgress } from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';
import type { AgentStatus } from '../../types';

interface AgentStatusIndicatorProps {
  status: AgentStatus;
}

export default function AgentStatusIndicator({ status }: AgentStatusIndicatorProps) {
  const getStatusConfig = () => {
    switch (status.status) {
      case 'processing':
        return {
          icon: <CircularProgress size={16} />,
          label: status.message || 'Agent processing...',
          color: 'info' as const,
        };
      case 'success':
        return {
          icon: <CheckCircleIcon />,
          label: status.message || 'Ready',
          color: 'success' as const,
        };
      case 'error':
        return {
          icon: <ErrorIcon />,
          label: status.message || 'Error - Check connection',
          color: 'error' as const,
        };
      default:
        return {
          icon: null,
          label: 'Idle',
          color: 'default' as const,
        };
    }
  };

  const config = getStatusConfig();

  return (
    <Chip
      icon={config.icon || undefined}
      label={config.label}
      color={config.color}
      size="small"
      sx={{ position: 'absolute', top: 16, right: 16 }}
    />
  );
}


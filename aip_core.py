#!/usr/bin/env python3
from __future__ import annotations
import torch, torch.nn as nn
import numpy as np

SEED = 42
torch.manual_seed(SEED)
np.random.seed(SEED)
PHI = (1 + 5**0.5) / 2
N_QUBITS = 16384
EMBED_SIZE = 128

class QuantumRISNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.a = nn.Parameter(torch.randn(EMBED_SIZE) * 0.5)
        self.b = nn.Parameter(torch.randn(EMBED_SIZE) * 0.5)
        self.c = nn.Parameter(torch.randn(EMBED_SIZE) * 0.5)
        self.aux = nn.Sequential(
            nn.Linear(EMBED_SIZE, EMBED_SIZE),
            nn.GELU(),
            nn.Linear(EMBED_SIZE, EMBED_SIZE)
        )

    def forward(self, flux: torch.Tensor, aux: torch.Tensor | None = None):
        x = flux.unsqueeze(-1) * self.a
        x += flux.unsqueeze(-1) * (PHI * 2) * self.b
        x += flux.unsqueeze(-1) * (PHI**2) * self.c
        if aux is not None:
            x += 0.5 * self.aux(aux)
        return x

def generate_quantum_ris(biometric_flux: np.ndarray | None = None) -> dict:
    device = "cuda" if torch.cuda.is_available() else "mps" if getattr(torch.backends,'mps',None) and torch.backends.mps.is_available() else "cpu"
    net = QuantumRISNet().to(device)

    if biometric_flux is not None:
        flux = torch.from_numpy(biometric_flux.astype(np.float32)).to(device)
        if flux.shape != (N_QUBITS,):
            raise ValueError(f"biometric_flux must have shape ({N_QUBITS},), got {flux.shape}")
        mode = "biometric"
    else:
        angles = torch.arange(N_QUBITS, device=device) * 2.399963029350463
        flux = 0.5 + 0.5 * torch.sin(angles * PHI)
        mode = "canonical"

    batch = flux.unsqueeze(0).repeat(1024, 1)
    aux = torch.randn(1024, EMBED_SIZE, device=device)

    with torch.no_grad():
        embedding = net(batch, aux)
        feature_vector = embedding.mean(0).cpu().numpy().astype(np.float64)

    quantum_spinor = np.tile(feature_vector, (N_QUBITS, 1))

    return {
        "version": "AIP-v3.0-prod",
        "mode": mode,
        "feature_vector": feature_vector,
        "quantum_spinor": quantum_spinor
    }

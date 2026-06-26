from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List
from interfaces.controllers.zoning_controller import ZoningController
from interfaces.serializers.zoning_schema import (
  ZoningRequestSchema,
  ZoningResponseSchema,
  OptimizationRequestSchema,
  OptimizationResponseSchema
)
from infrastructure.adapters.agdatabox_adapter import AgDataBoxAdapter
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
controller = ZoningController()

@router.post("/zoning", response_model=ZoningResponseSchema)
async def execute_zoning(
  request: ZoningRequestSchema,
  background_tasks: BackgroundTasks
):
  """
  Performs zoning based on geometric and operational constraints
  
  - **plot_id**: Plot ID in AgDataBox
  - **variables**: List of agronomic variables
  - **working_width**: Machine width (meters)
  - **sowing_direction**: Row direction (NS, EW, or CUSTOM)
  - **steering_angle**: Angle in degrees (if CUSTOM)
  - **n_zones_min/max**: Range of zones to test
  - **geometric_weight**: Spatial constraint weight (0-1)
  """
  try:
    result = controller.zoning_execute(request)
    
    # Save in the background if requested
    if request.salve_agdatabox:
      background_tasks.add_task(
        controller.agdatabox.zoning_save,
        request.plot_id,
        result.dict()
      )
    
    return result
      
  except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))
  except Exception as e:
    logger.error(f"Error in zoning: {str(e)}")
    raise HTTPException(status_code=500, detail=str(e))

@router.post("/zoning/optimize", response_model=OptimizationResponseSchema)
async def optimize_parameters(request: OptimizationRequestSchema):
  """
  Optimizes the number of zones and zoning parameters
  """
  try:
    return controller.optimize_parameters(request)
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))

@router.get("/plot")
async def list_plots(filters: dict = None):
  """List of available plots"""
  try:
    agbox = AgDataBoxAdapter()
    plots = agbox.list_plots(filters)
    return [
      {
        'id': t.id,
        'name': t.name,
        'area_hectares': t.area_hectares,
        'culture': t.culture,
        'harvest': t.harvest
      }
      for t in plots
    ]
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
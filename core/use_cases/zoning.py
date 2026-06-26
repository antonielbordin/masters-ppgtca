from typing import List, Dict, Optional
from core.entities.plot import Plot
from core.entities.sample_point import SamplePoint
from core.entities.zone import ZoningResult
from core.ports.agdatabox_port import AgDataBoxPort
from core.ports.algorithm_port import ZoningAlgorithmPort
from core.ports.repository_port import RepositoryPort
import logging

logger = logging.getLogger(__name__)

class ZoningUseCase:
  """
  Primary use case for restricted zoning
  """
  
  def __init__(
    self,
    agdatabox_port: AgDataBoxPort,
    algorithm_port: ZoningAlgorithmPort,
    repository_port: Optional[RepositoryPort] = None
  ):
    self.agdatabox = agdatabox_port
    self.algorithm = algorithm_port
    self.repository = repository_port
  
  def execute(
    self,
    plot_id: str,
    variables: List[str],
    working_width: float,
    sowing_direction: float,
    min_zones: int = 3,
    max_zones: int = 10,
    geometric_weight: float = 0.3,
    save_to_agdatabox: bool = True
  ) -> ZoningResult:
    """
    Executes the complete zoning pipeline
    """
    try:
      # 1. Validate input
      if n_zones_min < 2 or n_zones_max > 20:
        raise ValueError("Invalid number of zones")
      
      if not 0 <= geometric_weight <= 1:
        raise ValueError("The geometric weight must be between 0 and 1")
      
      # 2. Fetch data from AgDataBox
      logger.info(f"Fetching data for field {plot_id}")
      plot = self.agdatabox.get_plot(plot_id)
      points = self.agdatabox.get_agronomic_data(plot_id, variables)
      
      if not points:
        raise ValueError(f"No agronomic data found for field {plot_id}")
      
      logger.info(f"Retrieved {len(points)} sample points")
      
      # 3. Optimize number of zones
      logger.info("Optimizing number of zones")
      optimization = self.algorithm.optimize_parameters(
        points=points,
        working_width=working_width,
        seeding_direction=seeding_direction,
        n_zones_range=(n_zones_min, n_zones_max)
      )
      
      optimal_n_zones = optimization['n_zonas_otimo']
      logger.info(f"Optimal number of zones: {optimal_n_zones}")
      
      # 4. Execute zoning
      logger.info("Executing zoning")
      result = self.algorithm.execute(
        points=points,
        n_zones=optimal_n_zones,
        working_width=working_width,
        seeding_direction=seeding_direction,
        geometric_weight=geometric_weight
      )
      
      # 5. Save results
      if self.repository:
        self.repository.save_zoning(result)
      
      if salve_to_agdatabox:
        self._salve_to_agdatabox(plot_id, result)
      
      logger.info("Zoning successfully completed")
      return result
        
    except Exception as e:
      logger.error(f"Error in zoning: {str(e)}")
      raise
  
  def _save_to_agdatabox(self, plot_id: str, result: ZoningResult):
    """Saves the result to AgDataBox"""
    data = {
      'plot_id': plot_id,
      'n_zones': result.n_zones,
      'zones': self._dict_zones(result.zones),
      'metrics': result.metrics,
      'transitions_per_line': result.transitions_per_line,
      'explained_variability': result.explained_variability,
      'parameters': result.parameters_used
    }
    self.agdatabox.zoning_save(plot_id, data)
  
  def _zonas_para_dict(self, zones: List) -> List[Dict]:
    """Converts zones to a dictionary"""
    return [
      {
        'id': z.id,
        'index': z.index,
        'geometry': z.geometry.__geo_interface__,
        'average_attributes': z.average_attributes,
        'area_hectares': z.area_hectares
      }
      for z in zones
    ]
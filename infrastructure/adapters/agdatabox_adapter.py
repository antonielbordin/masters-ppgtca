import requests
import geopandas as gpd
from shapely.geometry import shape, Point, Polygon
from typing import List, Dict, Optional
from core.entities.plot import Plot
from core.entities.sample_point import SamplePoint
from core.ports.agdatabox_port import AgDataBoxPort
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

class AgDataBoxAdapter(AgDataBoxPort):
  """Concrete implementation of the adapter AgDataBox"""
  
  def __init__(self):
    self.base_url = settings.AGBOX_API_URL
    self.api_key = settings.AGBOX_API_KEY
    self.session = requests.Session()
    self.session.headers.update({
      "Authorization": f"Bearer {self.api_key}",
      "Content-Type": "application/json"
    })
  
  def list_plots(self, filters: Optional[Dict] = None) -> List[Plot]:
    """List of available plots"""
    endpoint = f"{self.base_url}talhoes"
    response = self.session.get(endpoint, params=filters)
    response.raise_for_status()
    
    data = response.json()
    plots = []
    for item in data:
      geometry = shape(item['geometria'])
      plots.append(
        Plot(
          id=item['id'],
          name=item['nome'],
          geometry=geometry,
          area_hectares=item['area_hectares'],
          harvest=item.get('safra', ''),
          culture=item.get('cultura', ''),
          creation_date=item['data_criacao']
        )
      )
    return plots
  
  def get_plot(self, plot_id: str) -> Plot:
    """Retrieves details of a plot"""
    plots = self.list_plots({'id': plot_id})
    if not plots:
      raise ValueError(f"Plot {plot_id} not found")
    return plots[0]
  
  def get_agronomic_data(self, plot_id: str, variables: List[str]) -> List[SamplePoint]:
    """Obtains agronomic data for the plot"""
    endpoint = f"{self.base_url}talhao/{plot_id}/dados"
    params = {"variables": ",".join(variables)}
    response = self.session.get(endpoint, params=params)
    response.raise_for_status()
    
    data = response.json()
    points = []
    for item in data['data']:
      geometry = Point(item['longitude'], item['latitude'])
      attributes = {var: item.get(var, 0) for var in variables}
      points.append(
        SamplePoint(
          id=item['id'],
          plot_id=plot_id,
          geometry=geometry,
          attributes=attributes,
          metadata=item.get('metadata', {})
        )
      )
    return points
  
  def zoning_save(self, plot_id: str, result: Dict) -> str:
    """Saves the zoning result to AgDataBox"""
    endpoint = f"{self.base_url}plots/{plot_id}/zoning"
    response = self.session.post(endpoint, json=result)
    response.raise_for_status()
    return response.json().get('id')
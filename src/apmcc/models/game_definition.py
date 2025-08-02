"""Data models for game definitions."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union


@dataclass
class Challenge:
    """Represents a challenge within a chapter."""
    name: str
    goal: bool = False
    excluded: bool = False
    priority: bool = False

    @classmethod
    def from_dict(cls, data: Dict[str, Union[str, bool]]) -> 'Challenge':
        """Create a Challenge from dictionary data."""
        return cls(
            name=data['name'],
            goal=data.get('goal', False),
            excluded=data.get('excluded', False),
            priority=data.get('priority', False)
        )


@dataclass
class Chapter:
    """Represents a chapter in the game."""
    name: str
    challenges: List[Challenge] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Union[str, List]]) -> 'Chapter':
        """Create a Chapter from dictionary data."""
        challenges = [
            Challenge.from_dict(challenge_data) 
            for challenge_data in data.get('challenges', [])
        ]
        return cls(
            name=data['name'],
            challenges=challenges
        )

    @property
    def goal_challenges(self) -> List[Challenge]:
        """Get all challenges marked as goal."""
        return [c for c in self.challenges if c.goal]

    @property
    def excluded_challenges(self) -> List[Challenge]:
        """Get all challenges marked as excluded."""
        return [c for c in self.challenges if c.excluded]

    @property
    def priority_challenges(self) -> List[Challenge]:
        """Get all challenges marked as priority."""
        return [c for c in self.challenges if c.priority]


@dataclass
class FillerItem:
    """Represents a filler item."""
    name: str
    weight: float = 1.0

    @classmethod
    def from_data(cls, data: Union[str, Dict[str, Union[str, float]]]) -> 'FillerItem':
        """Create a FillerItem from string or dictionary data."""
        if isinstance(data, str):
            return cls(name=data)
        return cls(
            name=data['name'],
            weight=data.get('weight', 1.0)
        )


@dataclass
class FillerItemCategory:
    """Represents a category of filler items."""
    name: str
    weight: float = 1.0
    include_confirmation_locations: bool = False
    items: List[FillerItem] = field(default_factory=list)

    @classmethod
    def from_dict(cls, name: str, data: Dict) -> 'FillerItemCategory':
        """Create a FillerItemCategory from dictionary data."""
        items = [
            FillerItem.from_data(item_data) 
            for item_data in data.get('items', [])
        ]
        return cls(
            name=name,
            weight=data.get('weight', 1.0),
            include_confirmation_locations=data.get('include_confirmation_locations', False),
            items=items
        )


@dataclass
class GameDefinition:
    """Represents the complete game definition."""
    name: str
    progression_items: List[str]
    chapters: List[Chapter]
    description: Optional[str] = None
    filler_item_categories: List[FillerItemCategory] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict) -> 'GameDefinition':
        """Create a GameDefinition from dictionary data."""
        chapters = [
            Chapter.from_dict(chapter_data) 
            for chapter_data in data.get('chapters', [])
        ]
        
        filler_categories = []
        if 'filler_item_categories' in data:
            for cat_name, cat_data in data['filler_item_categories'].items():
                filler_categories.append(
                    FillerItemCategory.from_dict(cat_name, cat_data)
                )
        
        return cls(
            name=data['name'],
            progression_items=data.get('progression_items', []),
            chapters=chapters,
            description=data.get('description'),
            filler_item_categories=filler_categories
        )

    @property
    def total_challenges(self) -> int:
        """Get total number of challenges across all chapters."""
        return sum(len(chapter.challenges) for chapter in self.chapters)

    @property
    def goal_challenges(self) -> List[Challenge]:
        """Get all challenges marked as goal across all chapters."""
        goals = []
        for chapter in self.chapters:
            goals.extend(chapter.goal_challenges)
        return goals

    @property
    def all_filler_items(self) -> List[FillerItem]:
        """Get all filler items from all categories."""
        items = []
        for category in self.filler_item_categories:
            items.extend(category.items)
        return items
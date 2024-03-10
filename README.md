<br />
<div align="center">
  <a href="https://github.com/jmroczkowski99/ownhoops">
    <img src="https://github.com/jmroczkowski99/ownhoops/assets/146372897/dc47904f-05c8-4bcd-ab2e-e525fec565fc" alt="Logo" width="240" height="240">
  </a>

<h3 align="center">ownhoops</h3>

  <p align="center">
    Basketball competition management REST API
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

RESTful API created for managing all types of basketball competitions. Enables creating, reading, updating and deleting teams, coaches, players, games and statlines. Provides calculating average stats and percentages, data validation and a lot of specific endpoints listed in Swagger UI based documentation. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* Django,
* Django REST Framework,
* Pytest,
* drf-spectacular,
* PostgreSQL,
* Docker.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

* Python 3.12 or higher,
* Git,
* Docker.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/jmroczkowski99/ownhoops.git
   ```
2. Create an .env file containing Django Secret Key, Postgres database info, and Debug value (won't work if DEBUG=True)
   ```
   SECRET_KEY=yoursecretkey
   DEBUG=False
   PG_USER=postgres
   PG_PASSWORD=postgres
   PG_DB=postgres
   PG_PORT=5432
   ```
3. Run Docker Compose
   ```sh
   docker compose up
   ```
4. Create a superuser to access features available only for authorized users
   ```sh
   docker exec -it python manage.py createsuperuser
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

### API documentation

You can access the Swagger UI based documentation and view all of the endpoints with provided examples at /schema/docs/ url.
<br />
<div align="center">
  <img src="https://github.com/jmroczkowski99/ownhoops/assets/146372897/3b44cf56-d787-4347-a03c-cf014d87b0c3" alt="Documentation">
</div>

### Teams

Example team .json response:
```json
{
    "url": "http://127.0.0.1:8000/teams/1/",
    "id": 1,
    "name_abbreviation": "MIA",
    "full_name": "Miami Heat",
    "coach": {
        "url": "http://127.0.0.1:8000/coaches/1/",
        "id": 1,
        "name": "Erik Spoelstra"
    },
    "players": [
        {
            "url": "http://127.0.0.1:8000/players/1/",
            "id": 1,
            "name": "Jimmy Butler",
            "position": "SF",
            "jersey_number": 22
        },
        {
            "url": "http://127.0.0.1:8000/players/2/",
            "id": 2,
            "name": "Nikola Jovic",
            "position": "PF",
            "jersey_number": 5
        },
        {
            "url": "http://127.0.0.1:8000/players/3/",
            "id": 3,
            "name": "Bam Adebayo",
            "position": "C",
            "jersey_number": 13
        },
        {
            "url": "http://127.0.0.1:8000/players/4/",
            "id": 4,
            "name": "Duncan Robinson",
            "position": "SG",
            "jersey_number": 55
        },
        {
            "url": "http://127.0.0.1:8000/players/5/",
            "id": 5,
            "name": "Terry Rozier",
            "position": "PG",
            "jersey_number": 2
        }
    ],
    "games": [
        {
            "url": "http://127.0.0.1:8000/games/1/",
            "id": 1,
            "info": "DET @ MIA - 2024-03-05T20:00:00Z",
            "box_score": "http://127.0.0.1:8000/games/1/stats/"
        },
        {
            "url": "http://127.0.0.1:8000/games/3/",
            "id": 3,
            "info": "MIA @ DAL - 2024-03-07T20:00:00Z",
            "box_score": "http://127.0.0.1:8000/games/3/stats/"
        }
    ]
}
```

To create a new Team instance you have to specify:
* Team name abbreviation - has to be 3 uppercase letters,
* Full Team name - every word has to start with an uppercase letter, but it can also contain numbers (i.e. Philadelphia 76ers).

Example valid input:
```json
{
    "name_abbreviation": "MIN",
    "full_name": "Minnesota Timberwolves"
}
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Coaches

Example coach .json response:
```json
{
    "url": "http://127.0.0.1:8000/coaches/1/",
    "id": 1,
    "name": "Erik Spoelstra",
    "date_of_birth": "1970-11-01",
    "team": "http://127.0.0.1:8000/teams/1/",
    "team_name_abbreviation": "MIA"
}
```

To create a new Coach instance you have to specify:
* Name - every word has to start with an uppercase letter, numbers and special characters are not allowed,
* Date of birth - has to be at least 18 years old,
* Team - can be blank.

Example valid input:
```json
{
    "name": "Billy Donovan",
    "date_of_birth": "1965-05-30",
    "team": "http://127.0.0.1:8000/teams/1/"
}
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Players

Example .json response:
```json
{
    "url": "http://127.0.0.1:8000/players/1/",
    "id": 1,
    "name": "Jimmy Butler",
    "team": "http://127.0.0.1:8000/teams/1/",
    "team_name_abbreviation": "MIA",
    "date_of_birth": "1989-09-14",
    "country": "USA",
    "position": "SF",
    "height": 201,
    "weight": 104,
    "jersey_number": 22,
    "points_per_game": 20.0,
    "offensive_rebounds_per_game": 1.0,
    "defensive_rebounds_per_game": 4.0,
    "rebounds_per_game": 5.0,
    "assists_per_game": 6.5,
    "steals_per_game": 2.0,
    "blocks_per_game": 0.0,
    "turnovers_per_game": 4.0,
    "field_goal_percentage": 52.0,
    "three_point_field_goal_percentage": 40.0,
    "free_throw_percentage": 85.71,
    "all_stats": "http://127.0.0.1:8000/players/1/stats/"
}
```

To create a new Player instance you have to specify:
* Name - every word has to start with an uppercase letter, numbers and special characters are not allowed,
* Team,
* Date of birth,
* Country - every word has to start with an uppercase letter. Numbers and special characters are not allowed, uppercase letters in the middle of country names are not allowed (exceptions: USA, DRF, UAE),
* Position - PG/SG/SF/PF/C,
* Height (in cm),
* Weight (in kg),
* Jersey number - has to be between 0 and 99, unique for a Team instance.

Example valid input:
```json
{
    "name": "Ausar Thompson",
    "team": "http://127.0.0.1:8000/teams/4/",
    "date_of_birth": "2003-01-30",
    "country": "USA",
    "position": "SF",
    "height": 198,
    "weight": 93,
    "jersey_number": 9
}
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Games

Example .json response:
```json
{
    "url": "http://127.0.0.1:8000/games/1/",
    "id": 1,
    "date": "2024-03-05T20:00:00Z",
    "game_info": "DET @ MIA - 2024-03-05 20:00:00+00:00",
    "home_team": "http://127.0.0.1:8000/teams/1/",
    "home_team_name_abbreviation": "MIA",
    "away_team": "http://127.0.0.1:8000/teams/4/",
    "away_team_name_abbreviation": "DET",
    "home_team_score": 87,
    "away_team_score": 75,
    "box_score": "http://127.0.0.1:8000/games/1/stats/"
}
```

To create a new Game instance you have to specify:
* Date - same team can't play two games in a span of 2 hours,
* Home Team,
* Away Team.

Example valid input:
```json
{
    "date": "2024-03-05 19:00:00",
    "home_team": "http://127.0.0.1:8000/teams/1/",
    "away_team": "http://127.0.0.1:8000/teams/4/"
}
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Stats
Example .json response:
```json
{
    "url": "http://127.0.0.1:8000/stats/1/",
    "id": 1,
    "game": "http://127.0.0.1:8000/games/1/",
    "game_info": "DET @ MIA - 2024-03-05 19:00:00+00:00",
    "player": "http://127.0.0.1:8000/players/1/",
    "player_name": "Jimmy Butler",
    "field_goals_made": 7,
    "field_goals_attempted": 13,
    "field_goal_percentage": 53.85,
    "three_pointers_made": 1,
    "three_pointers_attempted": 3,
    "three_point_percentage": 33.33,
    "free_throws_made": 11,
    "free_throws_attempted": 12,
    "free_throw_percentage": 91.67,
    "offensive_rebounds": 2,
    "defensive_rebounds": 4,
    "rebounds": 6,
    "assists": 8,
    "steals": 2,
    "blocks": 0,
    "turnovers": 2,
    "points": 26
}
```

To create a new Stats instance you have to specify:
* Game,
* Player - has to be a player of either home team or away team,
* Field goals made,
* Field goals attempted,
* Three pointers made,
* Three pointers attempted,
* Free throws made,
* Free throws attempted,
* Offensive rebounds,
* Defensive rebounds,
* Assists,
* Steals,
* Blocks,
* Turnovers.

Example valid input:
```json
{
    "game": "http://127.0.0.1:8000/games/1/",
    "player": "http://127.0.0.1:8000/players/1/",
    "field_goals_made": 7,
    "field_goals_attempted": 13,
    "three_pointers_made": 1,
    "three_pointers_attempted": 3,
    "free_throws_made": 11,
    "free_throws_attempted": 12,
    "offensive_rebounds": 2,
    "defensive_rebounds": 4,
    "assists": 8,
    "steals": 2,
    "blocks": 0,
    "turnovers": 2
}
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>
